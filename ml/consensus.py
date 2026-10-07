"""
ml/consensus.py
Group Consensus Engine — enhanced with:
  - Seasonal scoring (current month vs best travel time)
  - NB-derived per-destination sentiment score
  - Support for all 20 destinations
"""
import datetime
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

TYPE_TO_PREFERENCE = {
    "Beach":      "Pref_Beach",
    "Historical": "Pref_Historical",
    "Nature":     "Pref_Nature",
    "Adventure":  "Pref_Adventure",
    "City":       "Pref_City",
}

CLUSTER_PREFERENCE_COLUMNS = [
    "Pref_Beach", "Pref_Historical", "Pref_Nature", "Pref_Adventure", "Pref_City"
]

# Destination name → planning city for LR cost prediction
PLANNING_CITY_MAP = {
    "Goa Beaches":        "Goa",
    "Kovalam Beach":      "Trivandrum",
    "Andaman Islands":    "Port Blair",
    "Radhanagar Beach":   "Port Blair",
    "Taj Mahal":          "Agra",
    "Hampi Ruins":        "Bangalore",
    "Ajanta Ellora Caves":"Aurangabad",
    "Khajuraho Temples":  "Khajuraho",
    "Kerala Backwaters":  "Kerala",
    "Coorg":              "Coorg",
    "Munnar":             "Munnar",
    "Kaziranga":          "Kaziranga",
    "Leh Ladakh":         "Leh Ladakh",
    "Rishikesh":          "Rishikesh",
    "Manali":             "Manali",
    "Spiti Valley":       "Manali",
    "Jaipur City":        "Jaipur",
    "Varanasi":           "Varanasi",
    "Mysore":             "Mysore",
    "Kolkata":            "Kolkata",
}

# Month abbreviation → month number
_MONTH_MAP = {
    "jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
    "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12,
}

def _parse_best_months(best_time_str: str) -> list:
    """Convert 'Nov-Mar' → [11, 12, 1, 2, 3]."""
    if not best_time_str or pd.isna(best_time_str):
        return list(range(1, 13))
    parts = [p.strip().lower()[:3] for p in str(best_time_str).replace("–", "-").split("-")]
    if len(parts) != 2:
        return list(range(1, 13))
    start = _MONTH_MAP.get(parts[0])
    end   = _MONTH_MAP.get(parts[1])
    if start is None or end is None:
        return list(range(1, 13))
    if start <= end:
        return list(range(start, end + 1))
    else:
        return list(range(start, 13)) + list(range(1, end + 1))


def _seasonal_score(best_time_str: str, current_month: int = None) -> float:
    """Return 1.0 if current month is peak season, 0.3 if off-season."""
    if current_month is None:
        current_month = datetime.datetime.now().month
    best_months = _parse_best_months(best_time_str)
    return 1.0 if current_month in best_months else 0.3


class PackVoteEngine:
    """Loads trained models and runs the Group Consensus Engine."""

    def __init__(self):
        self.knn_model   = None
        self.knn_scaler  = None
        self.knn_columns = None
        self.dt_model    = None
        self.dt_columns  = None
        self.rf_model    = None
        self.rf_columns  = None
        self.lr_model    = None
        self.kmeans_model   = None
        self.kmeans_scaler  = None
        self.nb_model       = None
        self.nb_vectorizer  = None
        self.cf_scores      = None   # SVD collaborative filter scores
        self.sim_df         = None   # TF-IDF cosine similarity matrix
        self.destination_candidates      = None
        self.cluster_preference_profile  = None
        self._loaded = False

    def load(self):
        """Load all 8 models, destination candidates, and derived scores."""
        from ml.models import load_knn, load_dt, load_rf, load_lr, load_kmeans, load_nb, load_svd_cf, load_tfidf

        self.knn_model, self.knn_scaler, self.knn_columns = load_knn()
        self.dt_model, self.dt_columns = load_dt()
        self.rf_model, self.rf_columns = load_rf()
        self.rf_model.n_jobs = 1
        self.lr_model = load_lr()
        self.kmeans_model, self.kmeans_scaler, _ = load_kmeans()
        self.nb_model, self.nb_vectorizer = load_nb()
        _, self.cf_scores = load_svd_cf()
        _, self.sim_df    = load_tfidf()

        dest_file = PROCESSED_DIR / "destination_candidates.csv"
        self.destination_candidates = pd.read_csv(dest_file)

        cluster_file = PROCESSED_DIR / "traveler_cluster_profiles.csv"
        self.cluster_preference_profile = pd.read_csv(cluster_file, index_col=0)

        for col in CLUSTER_PREFERENCE_COLUMNS:
            if col not in self.cluster_preference_profile.columns:
                self.cluster_preference_profile[col] = 0.0

        # Compute per-destination sentiment score using NB on reviews
        self._compute_destination_sentiment()

        self._loaded = True
        return self


    def _compute_destination_sentiment(self):
        """Compute positive-review ratio per destination using the trained NB model."""
        reviews_file = PROCESSED_DIR / "reviews_ml.csv"
        if not reviews_file.exists():
            self.destination_candidates["Sentiment_Score"] = 0.5
            return

        reviews = pd.read_csv(reviews_file)
        if "ReviewText" not in reviews.columns or "DestinationID" not in reviews.columns:
            self.destination_candidates["Sentiment_Score"] = 0.5
            return

        try:
            texts = reviews["ReviewText"].fillna("").astype(str).tolist()
            X_vec = self.nb_vectorizer.transform(texts)
            preds = self.nb_model.predict(X_vec)
            reviews["NB_Positive"] = preds

            # Average positive ratio per destination (DestinationID 1-20)
            sent_map = (
                reviews.groupby("DestinationID")["NB_Positive"]
                .mean()
                .reset_index()
                .rename(columns={"NB_Positive": "Sentiment_Score"})
            )

            # Map back via DestinationID in destination_candidates
            self.destination_candidates = self.destination_candidates.merge(
                sent_map, on="DestinationID", how="left"
            )
            self.destination_candidates["Sentiment_Score"] = (
                self.destination_candidates["Sentiment_Score"].fillna(0.5)
            )
        except Exception:
            self.destination_candidates["Sentiment_Score"] = 0.5

    def _ensure_loaded(self):
        if not self._loaded:
            self.load()

    # ------------------------------------------------------------------
    # Input vector builders
    # ------------------------------------------------------------------

    def _create_knn_input(self, preference_text, destination_type, popularity,
                           adults=1, children=0):
        text = str(preference_text).lower()
        row = {
            "NumberOfAdults": adults,
            "NumberOfChildren": children,
            "Group_Size": adults + children,
            "Popularity": popularity,
            "Preference_Match": int(str(destination_type).lower() in text),
            "Pref_Beach":      int("beach"      in text),
            "Pref_Historical": int("historical" in text),
            "Pref_Nature":     int("nature"     in text),
            "Pref_Adventure":  int("adventure"  in text),
            "Pref_City":       int("city"       in text),
        }
        for col in self.knn_columns:
            if col.startswith("Type_"):
                row[col] = int(col.replace("Type_", "").lower() == str(destination_type).lower())
        result = pd.DataFrame([row]).reindex(columns=self.knn_columns, fill_value=0)
        return result.astype(float)

    def _create_dt_input(self, preference_text, destination_type, popularity,
                          adults=1, children=0):
        text = str(preference_text).lower()
        row = {
            "NumberOfAdults": adults,
            "NumberOfChildren": children,
            "Group_Size": adults + children,
            "Popularity": popularity,
            "Preference_Match": int(str(destination_type).lower() in text),
            "Pref_Beach":      int("beach"      in text),
            "Pref_Historical": int("historical" in text),
            "Pref_Nature":     int("nature"     in text),
            "Pref_Adventure":  int("adventure"  in text),
            "Pref_City":       int("city"       in text),
        }
        for col in self.dt_columns:
            if col.startswith("Type_"):
                row[col] = int(col.replace("Type_", "").lower() == str(destination_type).lower())
        result = pd.DataFrame([row]).reindex(columns=self.dt_columns, fill_value=0)
        return result.astype(float)

    # ------------------------------------------------------------------
    # Main recommendation function
    # ------------------------------------------------------------------

    def recommend_group(
        self,
        group_preferences: list,
        budget_per_person: float,
        accommodation_type: str = "Hotel",
        adults_per_traveler: int = 1,
        children_per_traveler: int = 0,
        current_month: int = None,
    ) -> pd.DataFrame:
        """
        Run the Group Consensus Engine.

        Scoring weights:
          0.25 × preference_match
          0.18 × experience_score        (KNN, normalized 0-1)
          0.18 × suitability_probability (Decision Tree)
          0.10 × rating_norm
          0.09 × popularity_norm
          0.10 × cluster_support         (K-Means)
          0.10 × sentiment_score         (NB positive ratio)  ← NEW

        Final group score:
          0.65 × avg_member_score
          0.15 × min_member_score        (least satisfied traveler)
          0.10 × budget_fit
          0.10 × seasonal_score          ← NEW
        """
        self._ensure_loaded()

        if not group_preferences:
            raise ValueError("At least one traveler preference is required.")

        if current_month is None:
            current_month = datetime.datetime.now().month

        # ── Precompute Traveler Cluster Supports and Preferences ──
        trav_pref_data = []
        for pref in group_preferences:
            p_str = str(pref).lower()
            prof_dict = {
                col: int(col.replace("Pref_", "").lower() in p_str)
                for col in CLUSTER_PREFERENCE_COLUMNS
            }
            # Distance to cluster centers
            diff = self.cluster_preference_profile[CLUSTER_PREFERENCE_COLUMNS] - pd.Series(prof_dict)
            nearest_cluster = (diff ** 2).sum(axis=1).idxmin()
            trav_pref_data.append({
                "pref_text": p_str,
                "nearest_cluster": nearest_cluster,
            })

        # ── Build Master Feature Matrix for all (destination, traveler) pairs ──
        knn_rows = []
        dt_rows = []
        pairs_meta = []

        for dest_idx, destination in self.destination_candidates.iterrows():
            dest_type = destination["Type"]
            popularity = float(destination["Popularity"])
            d_type_lower = str(dest_type).lower()

            for t_idx, t_data in enumerate(trav_pref_data):
                p_text = t_data["pref_text"]
                pref_match = int(d_type_lower in p_text)

                row = {
                    "NumberOfAdults": adults_per_traveler,
                    "NumberOfChildren": children_per_traveler,
                    "Group_Size": adults_per_traveler + children_per_traveler,
                    "Popularity": popularity,
                    "Preference_Match": pref_match,
                    "Pref_Beach": int("beach" in p_text),
                    "Pref_Historical": int("historical" in p_text),
                    "Pref_Nature": int("nature" in p_text),
                    "Pref_Adventure": int("adventure" in p_text),
                    "Pref_City": int("city" in p_text),
                }

                # One-hot type indicators
                for col in self.knn_columns:
                    if col.startswith("Type_"):
                        row[col] = int(col.replace("Type_", "").lower() == d_type_lower)

                knn_rows.append(row)
                dt_rows.append(row)
                pairs_meta.append((dest_idx, t_idx, pref_match))

        # ── High-Speed Batch Predictions ──
        df_knn = pd.DataFrame(knn_rows).reindex(columns=self.knn_columns, fill_value=0).astype(float)
        df_rf = pd.DataFrame(dt_rows).reindex(columns=self.rf_columns, fill_value=0).astype(float)
        df_dt = pd.DataFrame(dt_rows).reindex(columns=self.dt_columns, fill_value=0).astype(float)

        batch_knn_preds = np.clip(self.knn_model.predict(self.knn_scaler.transform(df_knn)), 1, 5)
        batch_rf_probs = self.rf_model.predict_proba(df_rf)[:, 1]
        batch_dt_probs = self.dt_model.predict_proba(df_dt)[:, 1]
        batch_suit_probs = 0.60 * batch_rf_probs + 0.40 * batch_dt_probs

        # ── Aggregate per Destination ──
        N_trav = len(group_preferences)
        results = []

        # CF score normalization bounds
        if self.cf_scores is not None and len(self.cf_scores) > 1:
            cf_min = float(self.cf_scores.min())
            cf_max = float(self.cf_scores.max())
        else:
            cf_min, cf_max = 0.0, 1.0

        for dest_idx, destination in self.destination_candidates.iterrows():
            dest_name = destination["Name"]
            dest_type = destination["Type"]
            popularity = float(destination["Popularity"])
            rating_norm = float(destination.get("Rating_Norm", 0))
            pop_norm = float(destination.get("Popularity_Norm", 0))
            sentiment = float(destination.get("Sentiment_Score", 0.5))

            # Seasonal score
            seasonal = _seasonal_score(destination.get("BestTimeToVisit", ""), current_month)

            # CF score
            dest_id = int(destination.get("DestinationID", 0))
            cf_raw = 0.0
            if self.cf_scores is not None:
                try:
                    cf_raw = float(self.cf_scores.get(dest_id, self.cf_scores.mean()))
                except Exception:
                    cf_raw = float(self.cf_scores.mean()) if len(self.cf_scores) else 0.0
            cf_norm = (cf_raw - cf_min) / (cf_max - cf_min + 1e-9) if cf_max > cf_min else 0.5

            # Slice batch predictions for this destination
            start_row = dest_idx * N_trav
            end_row = start_row + N_trav

            pred_exps = batch_knn_preds[start_row:end_row]
            suit_probs = batch_suit_probs[start_row:end_row]
            pref_matches = [pairs_meta[r][2] for r in range(start_row, end_row)]

            # Cluster support
            pref_col = TYPE_TO_PREFERENCE.get(dest_type)
            cluster_supports = []
            for t_data in trav_pref_data:
                if pref_col and pref_col in self.cluster_preference_profile.columns:
                    support = float(self.cluster_preference_profile.loc[t_data["nearest_cluster"], pref_col])
                else:
                    support = 0.5
                cluster_supports.append(support)

            # Compute individual scores
            individual_scores = []
            for i in range(N_trav):
                exp_score = (pred_exps[i] - 1) / 4
                s = 100 * (
                    0.22 * pref_matches[i]
                    + 0.16 * exp_score
                    + 0.16 * suit_probs[i]
                    + 0.10 * rating_norm
                    + 0.08 * pop_norm
                    + 0.10 * cluster_supports[i]
                    + 0.10 * sentiment
                    + 0.08 * cf_norm
                )
                individual_scores.append(s)

            avg_score = float(np.mean(individual_scores))
            min_score = float(np.min(individual_scores))
            grp_pref = float(np.mean(pref_matches))
            clust_cons = float(np.mean(cluster_supports))

            # Budget via LR
            predicted_cost = np.nan
            budget_fit = 0.5
            budget_status = "Cost data unavailable"
            planning_city = PLANNING_CITY_MAP.get(dest_name)

            if planning_city:
                try:
                    cost_input = pd.DataFrame({
                        "City": [planning_city],
                        "Accomadation_Type": [accommodation_type],
                    })
                    predicted_cost = float(max(0, self.lr_model.predict(cost_input)[0]))
                    if predicted_cost <= budget_per_person:
                        budget_fit = 1.0
                        budget_status = "Within budget"
                    else:
                        budget_fit = float(np.clip(budget_per_person / (predicted_cost + 1e-9), 0, 1))
                        budget_status = "Above budget"
                except Exception:
                    budget_status = "Cost prediction unavailable"

            # Final Group Consensus Score
            final_score = (
                0.65 * avg_score
                + 0.15 * min_score
                + 0.10 * (budget_fit * 100)
                + 0.10 * (seasonal * 100)
            )

            results.append({
                "Destination":             dest_name,
                "State":                   destination["State"],
                "Type":                    dest_type,
                "Group_Compatibility":     round(final_score, 2),
                "Average_Member_Score":    round(avg_score, 2),
                "Minimum_Member_Score":    round(min_score, 2),
                "Group_Preference_Match":  round(grp_pref * 100, 2),
                "KMeans_Cluster_Support":  round(clust_cons * 100, 2),
                "Predicted_Experience":    round(float(np.mean(pred_exps)), 2),
                "Suitability":             round(float(np.mean(suit_probs)) * 100, 2),
                "Popularity":              round(popularity, 2),
                "Average_Rating":          round(float(destination.get("Avg_Rating", 0)), 2),
                "Sentiment_Score":         round(sentiment * 100, 2),
                "Seasonal_Score":          round(seasonal * 100, 2),
                "In_Peak_Season":          seasonal == 1.0,
                "Best_Time":               destination.get("BestTimeToVisit", "Unknown"),
                "Planning_City":           planning_city,
                "Description":             destination.get("Description", ""),
                "Predicted_Accommodation_Cost": (
                    round(predicted_cost, 2) if not np.isnan(predicted_cost) else None
                ),
                "Budget_Fit":    round(budget_fit * 100, 2),
                "Budget_Status": budget_status,
            })

        result_df = (
            pd.DataFrame(results)
            .sort_values("Group_Compatibility", ascending=False)
            .reset_index(drop=True)
        )
        result_df["Rank"] = result_df.index + 1
        cols = ["Rank"] + [c for c in result_df.columns if c != "Rank"]
        return result_df[cols]


# Singleton
_engine = None

def get_engine() -> PackVoteEngine:
    global _engine
    if _engine is None:
        _engine = PackVoteEngine()
        _engine.load()
    return _engine

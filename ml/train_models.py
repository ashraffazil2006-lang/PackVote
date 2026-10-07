"""
ml/train_models.py
One-shot training script for all 8 ML models.
Usage: python ml/train_models.py
"""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ml.preprocessing import preprocess_all
from ml.features import build_all_features
from ml.models import (
    train_kmeans, save_kmeans,
    train_knn, save_knn,
    train_decision_tree, save_dt,
    train_random_forest, save_rf,
    train_naive_bayes, save_nb,
    train_linear_regression, save_lr,
    train_svd_cf, save_svd_cf,
    train_tfidf_similarity, save_tfidf,
)
from ml.tourist_spots import load_citywise_attractions, save_attractions_table

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
MODELS_DIR    = Path(__file__).resolve().parent.parent / "models"


def main():
    print("=" * 60)
    print("PACKVOTE — Training All 8 ML Models")
    print("=" * 60)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. PREPROCESSING
    print("\n[1/9] Preprocessing datasets...")
    data = preprocess_all(save=True)
    print(f"      Users:        {data['users_p'].shape}")
    print(f"      Destinations: {data['destinations_p'].shape}")
    print(f"      Reviews ML:   {data['reviews_ml'].shape}")
    print(f"      User History: {data['user_history_p'].shape}")
    print(f"      Travel Cost:  {data['travel_cost_p'].shape}")
    print(f"      Tourist Spots:{data['tourist_spots_p'].shape}")

    # 2. FEATURE ENGINEERING
    print("\n[2/9] Building features...")
    features = build_all_features(data)
    print(f"      Traveler features:     {features['traveler_features'].shape}")
    print(f"      Interaction features:  {features['interaction_features'].shape}")
    print(f"      KNN features:          {features['knn_features'].shape}")
    print(f"      DT features:           {features['X_dt'].shape}")
    print(f"      NB (TF-IDF):           {features['X_nb'].shape}")
    print(f"      LR features:           {features['X_lr'].shape}")

    # 3. K-MEANS
    print("\n[3/9] Training K-Means (Traveler Profiling)...")
    km_model, km_scaler, traveler_with_clusters, cluster_profile, km_metrics = train_kmeans(
        features["traveler_features"], n_clusters=4
    )
    save_kmeans(km_model, km_scaler, traveler_with_clusters, cluster_profile)
    print(f"      K-Means: k={km_metrics['n_clusters']}, inertia={km_metrics['inertia']}")

    # 4. KNN
    print("\n[4/9] Training KNN (Experience Predictor)...")
    knn_model, knn_scaler, knn_cols, knn_metrics = train_knn(
        features["knn_features"], features["knn_target"]
    )
    save_knn(knn_model, knn_scaler, knn_cols)
    print(f"      KNN: k={knn_metrics['best_k']}, MAE={knn_metrics['MAE']}, R2={knn_metrics['R2']}")

    # 5. DECISION TREE
    print("\n[5/9] Training Decision Tree (Baseline Suitability)...")
    dt_model, dt_cols, dt_metrics = train_decision_tree(features["X_dt"], features["y_dt"])
    save_dt(dt_model, dt_cols)
    print(f"      DT: depth={dt_metrics['best_depth']}, Acc={dt_metrics['Accuracy']}, F1={dt_metrics['F1']}")

    # 6. RANDOM FOREST
    print("\n[6/9] Training Random Forest (Ensemble Suitability)...")
    rf_model, rf_cols, rf_metrics = train_random_forest(features["X_dt"], features["y_dt"])
    save_rf(rf_model, rf_cols)
    print(f"      RF: n={rf_metrics['best_n_estimators']}, Acc={rf_metrics['Accuracy']}, F1={rf_metrics['F1']}")

    # 7. NAIVE BAYES
    print("\n[7/9] Training Naive Bayes (Review Sentiment)...")
    nb_model, nb_metrics = train_naive_bayes(features["X_nb"], features["y_nb"])
    save_nb(nb_model, features["nb_vectorizer"])
    print(f"      NB: alpha={nb_metrics['best_alpha']}, Acc={nb_metrics['Accuracy']}, F1={nb_metrics['F1']}")

    # 8. LINEAR REGRESSION
    print("\n[8a/9] Training Linear Regression (Accommodation Cost)...")
    lr_model, lr_metrics = train_linear_regression(features["X_lr"], features["y_lr"])
    save_lr(lr_model)
    print(f"      LR: MAE={lr_metrics['MAE']}, R2={lr_metrics['R2']}")

    # 8b. Build destination candidates (needed for SVD + TF-IDF)
    print("\n[8b/9] Building destination candidates table...")
    destinations_p = data["destinations_p"]
    reviews_ml     = data["reviews_ml"]
    travel_cost_p  = data["travel_cost_p"]

    # Add description from destinations if available
    desc_cols = ["Name", "State", "Type", "BestTimeToVisit", "DestinationID", "Popularity"]
    if "Description" in destinations_p.columns:
        desc_cols.append("Description")

    destination_candidates = (
        destinations_p
        .groupby(["Name", "State", "Type", "BestTimeToVisit"], as_index=False)
        .agg(
            DestinationID=("DestinationID", "first"),
            Popularity=("Popularity", "mean"),
            **({ "Description": ("Description", "first") } if "Description" in destinations_p.columns else {}),
        )
    )

    destination_rating = (
        reviews_ml
        .merge(destinations_p[["DestinationID", "Name"]], on="DestinationID", how="left")
        .groupby("Name")
        .agg(Avg_Rating=("Rating", "mean"), Review_Count=("ReviewID", "count"))
        .reset_index()
    )
    destination_candidates = destination_candidates.merge(destination_rating, on="Name", how="left")
    destination_candidates[["Avg_Rating", "Review_Count"]] = (
        destination_candidates[["Avg_Rating", "Review_Count"]].fillna(0)
    )

    pop_min = destination_candidates["Popularity"].min()
    pop_max = destination_candidates["Popularity"].max()
    destination_candidates["Popularity_Norm"] = (
        destination_candidates["Popularity"] - pop_min
    ) / (pop_max - pop_min + 1e-9)
    destination_candidates["Rating_Norm"] = destination_candidates["Avg_Rating"] / 5

    city_cost_summary = (
        travel_cost_p[travel_cost_p["Cost_Average"].notna()]
        .groupby("City", as_index=False)
        .agg(Cost_Min=("Cost_Min","min"), Cost_Max=("Cost_Max","max"), Cost_Average=("Cost_Average","mean"))
    )

    from ml.consensus import PLANNING_CITY_MAP
    destination_candidates["Planning_City"] = destination_candidates["Name"].map(PLANNING_CITY_MAP)
    destination_candidates = destination_candidates.merge(
        city_cost_summary, left_on="Planning_City", right_on="City", how="left"
    ).drop(columns=["City"], errors="ignore")

    destination_candidates.to_csv(PROCESSED_DIR / "destination_candidates.csv", index=False)
    print(f"      Destination candidates: {destination_candidates.shape}")
    print(f"      Destinations: {sorted(destination_candidates['Name'].unique().tolist())}")

    # 9a. SVD COLLABORATIVE FILTERING
    print("\n[9a/9] Training SVD Collaborative Filter...")
    svd_model, U, V, user_ids, dest_ids, dest_cf_scores, svd_metrics = train_svd_cf(
        data["user_history_p"], n_components=15
    )
    save_svd_cf(svd_model, dest_cf_scores)
    print(f"      SVD: {svd_metrics['n_components']} components, "
          f"variance={svd_metrics['explained_variance_ratio']:.3f}, "
          f"{svd_metrics['n_users']} users × {svd_metrics['n_destinations']} destinations")

    # 9b. TF-IDF SIMILARITY
    print("\n[9b/9] Training TF-IDF Destination Similarity...")
    tfidf_vec, sim_df, tfidf_metrics = train_tfidf_similarity(destination_candidates)
    save_tfidf(tfidf_vec, sim_df)
    print(f"      TF-IDF: {tfidf_metrics['n_destinations']} destinations, "
          f"vocab={tfidf_metrics['vocab_size']}")

    # Citywise attractions
    print("\n[Extra] Building citywise attractions table...")
    attractions = load_citywise_attractions()
    save_attractions_table(attractions)
    print(f"      Attractions: {len(attractions)} rows")

    # Save metrics
    metrics = {
        "kmeans":             km_metrics,
        "knn":                knn_metrics,
        "decision_tree":      dt_metrics,
        "random_forest":      rf_metrics,
        "naive_bayes":        nb_metrics,
        "linear_regression":  lr_metrics,
        "svd_cf":             svd_metrics,
        "tfidf_similarity":   tfidf_metrics,
    }
    with open(PROCESSED_DIR / "model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE — All 8 models saved to /models/")
    print("=" * 60)
    print("\nModel metrics:")
    for name, m in metrics.items():
        print(f"  {name}: {m}")

    return metrics


if __name__ == "__main__":
    main()

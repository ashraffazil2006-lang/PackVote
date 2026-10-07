"""
ml/features.py
Feature engineering — faithful to notebook Step 6.
"""
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path

PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"


def build_traveler_features(users_p, user_history_p, reviews_ml):
    """Build traveler feature matrix (K-Means input)."""
    experience_features = (
        user_history_p.groupby("UserID")
        .agg(
            Avg_Experience=("ExperienceRating", "mean"),
            Visit_Count=("DestinationID", "count"),
        )
        .reset_index()
    )

    review_features = (
        reviews_ml.groupby("UserID")
        .agg(
            Avg_Review_Rating=("Rating", "mean"),
            Review_Count=("ReviewID", "count"),
        )
        .reset_index()
    )

    traveler_features = users_p[
        [
            "UserID",
            "NumberOfAdults",
            "NumberOfChildren",
            "Pref_Beach",
            "Pref_Historical",
            "Pref_Nature",
            "Pref_Adventure",
            "Pref_City",
        ]
    ].copy()

    traveler_features["Group_Size"] = (
        traveler_features["NumberOfAdults"] + traveler_features["NumberOfChildren"]
    )

    traveler_features = (
        traveler_features
        .merge(experience_features, on="UserID", how="left")
        .merge(review_features, on="UserID", how="left")
    )

    for col in ["Avg_Experience", "Visit_Count", "Avg_Review_Rating", "Review_Count"]:
        traveler_features[col] = traveler_features[col].fillna(0)

    return traveler_features


def build_destination_features(destinations_p, reviews_ml):
    """Build destination feature matrix."""
    destination_features = destinations_p[
        ["DestinationID", "Name", "State", "Type", "Popularity", "BestTimeToVisit"]
    ].copy()

    destination_type_features = pd.get_dummies(
        destination_features["Type"], prefix="Type", dtype=int
    )

    destination_features = pd.concat([destination_features, destination_type_features], axis=1)

    pop_min = destination_features["Popularity"].min()
    pop_max = destination_features["Popularity"].max()
    destination_features["Popularity_Norm"] = (
        destination_features["Popularity"] - pop_min
    ) / (pop_max - pop_min + 1e-9)

    destination_rating_features = (
        reviews_ml
        .merge(destinations_p[["DestinationID", "Name"]], on="DestinationID", how="left")
        .groupby(["DestinationID", "Name"])
        .agg(Avg_Rating=("Rating", "mean"), Rating_Count=("ReviewID", "count"))
        .reset_index()
    )
    destination_rating_features["Rating_Norm"] = destination_rating_features["Avg_Rating"] / 5

    destination_features = destination_features.merge(
        destination_rating_features, on=["DestinationID", "Name"], how="left"
    )
    destination_features[["Avg_Rating", "Rating_Count", "Rating_Norm"]] = (
        destination_features[["Avg_Rating", "Rating_Count", "Rating_Norm"]].fillna(0)
    )

    return destination_features


def build_interaction_features(users_p, user_history_p, destinations_p):
    """Build user-destination interaction features."""
    interaction_features = (
        user_history_p[["UserID", "DestinationID", "ExperienceRating", "VisitDate"]]
        .merge(
            users_p[["UserID", "Preferences_Clean", "NumberOfAdults", "NumberOfChildren"]],
            on="UserID",
            how="left",
        )
        .merge(
            destinations_p[["DestinationID", "Name", "State", "Type", "Popularity"]],
            on="DestinationID",
            how="left",
        )
    )

    interaction_features["Group_Size"] = (
        interaction_features["NumberOfAdults"] + interaction_features["NumberOfChildren"]
    )

    interaction_features["Preference_Match"] = interaction_features.apply(
        lambda row: int(
            str(row["Type"]).lower() in str(row["Preferences_Clean"]).lower()
        ),
        axis=1,
    )

    interaction_features["Suitable"] = (
        interaction_features["ExperienceRating"] >= 4
    ).astype(int)

    return interaction_features


def build_knn_features(interaction_features):
    """Build leakage-free KNN feature matrix (no ExperienceRating as input)."""
    pref_features = interaction_features["Preferences_Clean"].apply(
        lambda text: pd.Series(
            {
                "Pref_Beach": int("beach" in str(text).lower()),
                "Pref_Historical": int("historical" in str(text).lower()),
                "Pref_Nature": int("nature" in str(text).lower()),
                "Pref_Adventure": int("adventure" in str(text).lower()),
                "Pref_City": int("city" in str(text).lower()),
            }
        )
    )

    type_features = pd.get_dummies(interaction_features["Type"], prefix="Type", dtype=int)

    knn_features = pd.concat(
        [
            interaction_features[
                ["NumberOfAdults", "NumberOfChildren", "Group_Size", "Popularity", "Preference_Match"]
            ].reset_index(drop=True),
            pref_features.reset_index(drop=True),
            type_features.reset_index(drop=True),
        ],
        axis=1,
    )

    knn_features = knn_features.replace([np.inf, -np.inf], np.nan).fillna(0)
    knn_target = interaction_features["ExperienceRating"].astype(float).reset_index(drop=True)

    valid_rows = knn_target.notna()
    knn_features = knn_features.loc[valid_rows].reset_index(drop=True)
    knn_target = knn_target.loc[valid_rows].reset_index(drop=True)

    return knn_features, knn_target


def build_dt_features(interaction_features):
    """Build Decision Tree feature matrix."""
    dt_pref = interaction_features["Preferences_Clean"].apply(
        lambda text: pd.Series(
            {
                "Pref_Beach": int("beach" in str(text).lower()),
                "Pref_Historical": int("historical" in str(text).lower()),
                "Pref_Nature": int("nature" in str(text).lower()),
                "Pref_Adventure": int("adventure" in str(text).lower()),
                "Pref_City": int("city" in str(text).lower()),
            }
        )
    )

    dt_type = pd.get_dummies(interaction_features["Type"], prefix="Type", dtype=int)

    dt_numeric = interaction_features[
        ["NumberOfAdults", "NumberOfChildren", "Group_Size", "Popularity", "Preference_Match"]
    ].copy()

    X_dt = pd.concat(
        [
            dt_numeric.reset_index(drop=True),
            dt_pref.reset_index(drop=True),
            dt_type.reset_index(drop=True),
        ],
        axis=1,
    )

    y_dt = interaction_features["Suitable"].astype(int).reset_index(drop=True)
    X_dt = X_dt.replace([np.inf, -np.inf], np.nan).fillna(0)

    return X_dt, y_dt


def build_nb_features(reviews_ml):
    """Build Naive Bayes TF-IDF feature matrix for review sentiment."""
    nb_data = reviews_ml[["ReviewID", "ReviewText", "Rating"]].copy()
    nb_data["ReviewText"] = (
        nb_data["ReviewText"].fillna("").astype(str).str.strip()
    )
    nb_data = nb_data[nb_data["ReviewText"] != ""].copy()
    nb_data["Review_Label"] = (nb_data["Rating"] >= 4).astype(int)

    vectorizer = TfidfVectorizer(
        max_features=1000, ngram_range=(1, 2), min_df=1, stop_words="english"
    )
    X_nb = vectorizer.fit_transform(nb_data["ReviewText"].astype(str))
    y_nb = nb_data["Review_Label"]

    return X_nb, y_nb, vectorizer, nb_data


def build_lr_features(travel_cost_p):
    """Build Linear Regression features for accommodation cost prediction."""
    lr_data = travel_cost_p[["City", "Accomadation_Type", "Cost_Average"]].copy()
    lr_data["Cost_Average"] = pd.to_numeric(lr_data["Cost_Average"], errors="coerce")
    lr_data = lr_data[lr_data["Cost_Average"].notna()].copy()
    lr_data = lr_data[lr_data["Cost_Average"] >= 0].copy()

    X_lr = lr_data[["City", "Accomadation_Type"]]
    y_lr = lr_data["Cost_Average"]

    return X_lr, y_lr


def build_tourist_features(tourist_spots_p):
    """Build tourist spot features."""
    tourist_features = tourist_spots_p.copy()
    tourist_features["Characteristic_Count"] = (
        tourist_features["Characteristics"]
        .fillna("")
        .apply(lambda x: len([item for item in str(x).split(",") if item.strip()]))
    )
    tourist_features["Has_Nature"] = (
        tourist_features["Characteristics"]
        .str.contains("nature|scenic|greenery|waterfall", case=False, na=False)
        .astype(int)
    )
    tourist_features["Has_Adventure"] = (
        tourist_features["Characteristics"]
        .str.contains("adventure|trekking|hiking|zipline", case=False, na=False)
        .astype(int)
    )
    tourist_features["Has_Historical"] = (
        tourist_features["Characteristics"]
        .str.contains("historical|heritage|temple|fort", case=False, na=False)
        .astype(int)
    )
    tourist_features["Has_Family"] = (
        tourist_features["Characteristics"]
        .str.contains("family|amusement", case=False, na=False)
        .astype(int)
    )

    tourist_summary = (
        tourist_features.groupby("DestinationID")
        .agg(
            Tourist_Spot_Count=("Name", "count"),
            Nature_Spot_Count=("Has_Nature", "sum"),
            Adventure_Spot_Count=("Has_Adventure", "sum"),
            Historical_Spot_Count=("Has_Historical", "sum"),
            Family_Spot_Count=("Has_Family", "sum"),
        )
        .reset_index()
    )

    return tourist_features, tourist_summary


def build_all_features(data):
    """
    Build all feature matrices from preprocessed data.
    Returns dict of feature tables.
    """
    users_p = data["users_p"]
    destinations_p = data["destinations_p"]
    reviews_ml = data["reviews_ml"]
    user_history_p = data["user_history_p"]
    travel_cost_p = data["travel_cost_p"]
    tourist_spots_p = data["tourist_spots_p"]

    traveler_features = build_traveler_features(users_p, user_history_p, reviews_ml)
    destination_features = build_destination_features(destinations_p, reviews_ml)
    interaction_features = build_interaction_features(users_p, user_history_p, destinations_p)
    knn_features, knn_target = build_knn_features(interaction_features)
    X_dt, y_dt = build_dt_features(interaction_features)
    X_nb, y_nb, nb_vectorizer, nb_data = build_nb_features(reviews_ml)
    X_lr, y_lr = build_lr_features(travel_cost_p)
    tourist_features, tourist_summary = build_tourist_features(tourist_spots_p)

    return {
        "traveler_features": traveler_features,
        "destination_features": destination_features,
        "interaction_features": interaction_features,
        "knn_features": knn_features,
        "knn_target": knn_target,
        "X_dt": X_dt,
        "y_dt": y_dt,
        "X_nb": X_nb,
        "y_nb": y_nb,
        "nb_vectorizer": nb_vectorizer,
        "nb_data": nb_data,
        "X_lr": X_lr,
        "y_lr": y_lr,
        "tourist_features": tourist_features,
        "tourist_summary": tourist_summary,
    }

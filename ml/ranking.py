"""
ml/ranking.py
Destination ranking + rich "Why This Destination?" explanation.
Enhanced with seasonal and sentiment signals.
"""
import pandas as pd
import numpy as np


def create_reason(row: dict) -> str:
    """Generate a detailed human-readable explanation for a destination recommendation."""
    reasons = []

    pref_score    = float(row.get("Group_Preference_Match", 0))
    suit_score    = float(row.get("Suitability", 0))
    exp_score     = float(row.get("Predicted_Experience", 0))
    rating_score  = float(row.get("Average_Rating", 0))
    budget_status = row.get("Budget_Status", "Cost data unavailable")
    cluster_supp  = float(row.get("KMeans_Cluster_Support", 0))
    sentiment     = float(row.get("Sentiment_Score", 50))
    in_season     = row.get("In_Peak_Season", False)
    seasonal      = float(row.get("Seasonal_Score", 50))

    # Preference match
    if pref_score >= 75:
        reasons.append("strong match with the group's travel preferences")
    elif pref_score >= 50:
        reasons.append("good match with the group's travel preferences")
    else:
        reasons.append("partial match with the group's preferences")

    # Suitability
    if suit_score >= 70:
        reasons.append("high destination suitability for your traveler profiles")
    elif suit_score >= 50:
        reasons.append("moderate destination suitability")

    # Predicted experience
    if exp_score >= 4.2:
        reasons.append("exceptional predicted experience rating")
    elif exp_score >= 3.5:
        reasons.append("good predicted experience rating")

    # Ratings
    if rating_score >= 4.2:
        reasons.append("highly rated by previous visitors")
    elif rating_score >= 3.5:
        reasons.append("well reviewed by previous visitors")

    # Budget
    if budget_status == "Within budget":
        reasons.append("comfortably fits the group's budget")
    elif budget_status == "Above budget":
        reasons.append("slightly above budget but offers exceptional value")

    # K-Means cluster alignment
    if cluster_supp >= 60:
        reasons.append("strongly aligned with your traveler profile clusters")
    elif cluster_supp >= 35:
        reasons.append("supported by similar traveler profiles")

    # NB Sentiment
    if sentiment >= 70:
        reasons.append("highly positive reviews from past travelers")
    elif sentiment >= 55:
        reasons.append("generally positive traveler sentiment")

    # Seasonal fit
    if in_season:
        reasons.append("currently in its peak travel season")
    elif seasonal <= 30:
        reasons.append("note: this is off-peak season — expect fewer crowds")

    if not reasons:
        reasons.append("recommended by the PACKVOTE consensus algorithm")

    return "Selected because: " + ", ".join(reasons) + "."


def add_explanations(recommendations: pd.DataFrame) -> pd.DataFrame:
    recommendations = recommendations.copy()
    recommendations["Why_This_Destination"] = recommendations.apply(
        lambda row: create_reason(row.to_dict()), axis=1
    )
    return recommendations


def rank_recommendations(recommendations: pd.DataFrame) -> pd.DataFrame:
    """Sort by Group_Compatibility, assign ranks, add explanations."""
    ranked = (
        recommendations
        .sort_values("Group_Compatibility", ascending=False)
        .reset_index(drop=True)
    )
    ranked["Rank"] = ranked.index + 1

    if "Budget_Fit" not in ranked.columns:
        ranked["Budget_Fit"] = np.where(ranked.get("Budget_Status", pd.Series()).eq("Within budget"), 100.0, 0.0)

    ranked = add_explanations(ranked)

    preferred_order = [
        "Rank", "Destination", "State", "Type", "Description",
        "Group_Compatibility", "Group_Preference_Match",
        "KMeans_Cluster_Support", "Predicted_Experience", "Suitability",
        "Average_Rating", "Popularity", "Sentiment_Score", "Seasonal_Score",
        "In_Peak_Season", "Budget_Status", "Budget_Fit",
        "Predicted_Accommodation_Cost", "Best_Time", "Why_This_Destination",
        "Planning_City", "Average_Member_Score", "Minimum_Member_Score",
    ]
    cols = [c for c in preferred_order if c in ranked.columns]
    remaining = [c for c in ranked.columns if c not in cols]
    return ranked[cols + remaining]

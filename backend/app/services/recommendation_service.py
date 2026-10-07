"""
backend/app/services/recommendation_service.py
Service layer for recommendation business logic.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))

from ml.predict import get_recommendations
from backend.app.schemas import RecommendationItem, TouristSpot


def build_recommendations(
    travelers: list,
    budget_per_person: float,
    accommodation_type: str,
    top_n: int = 5,
) -> list:
    """
    Convert API request into ML predictions and format response.

    Parameters
    ----------
    travelers : list of TravelerInput
    budget_per_person : float
    accommodation_type : str
    top_n : int

    Returns
    -------
    list of RecommendationItem
    """
    # Build group preferences string list
    group_preferences = []
    for traveler in travelers:
        prefs = traveler.preferences
        if isinstance(prefs, list):
            pref_str = ", ".join(prefs)
        else:
            pref_str = str(prefs)
        group_preferences.append(pref_str)

    # Run ML pipeline
    raw_results = get_recommendations(
        group_preferences=group_preferences,
        budget_per_person=budget_per_person,
        accommodation_type=accommodation_type,
        top_n=top_n,
    )

    # Format response
    recommendations = []
    for item in raw_results:
        spots = []
        for spot in item.get("Tourist_Spots", []):
            spots.append(TouristSpot(
                name=spot.get("name", "Unknown"),
                characteristics=spot.get("characteristics"),
                latitude=spot.get("latitude"),
                longitude=spot.get("longitude"),
                source=spot.get("source"),
            ))

        rec = RecommendationItem(
            rank=int(item.get("Rank", 0)),
            destination=str(item.get("Destination", "")),
            state=str(item.get("State", "")),
            destination_type=str(item.get("Type", "")),
            description=item.get("Description") or None,
            group_compatibility=float(item.get("Group_Compatibility", 0)),
            group_preference_match=float(item.get("Group_Preference_Match", 0)),
            kmeans_cluster_support=float(item.get("KMeans_Cluster_Support", 0)),
            predicted_experience=float(item.get("Predicted_Experience", 0)),
            suitability=float(item.get("Suitability", 0)),
            average_rating=float(item.get("Average_Rating", 0)),
            popularity=float(item.get("Popularity", 0)),
            sentiment_score=float(item.get("Sentiment_Score", 50)) if item.get("Sentiment_Score") is not None else None,
            seasonal_score=float(item.get("Seasonal_Score", 50)) if item.get("Seasonal_Score") is not None else None,
            in_peak_season=bool(item.get("In_Peak_Season", False)),
            budget_status=str(item.get("Budget_Status", "Unknown")),
            budget_fit=float(item.get("Budget_Fit", 0)),
            predicted_accommodation_cost=item.get("Predicted_Accommodation_Cost"),
            best_time=str(item.get("Best_Time", "Unknown")),
            why_this_destination=str(item.get("Why_This_Destination", "")),
            tourist_spots=spots,
            total_spots=len(spots),
        )
        recommendations.append(rec)

    return recommendations

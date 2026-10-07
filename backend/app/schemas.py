"""
backend/app/schemas.py
Pydantic schemas for request and response models.
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


# ============================================================
# REQUEST MODELS
# ============================================================

class TravelerInput(BaseModel):
    preferences: List[str] = Field(
        ...,
        description="Traveler preference categories",
        examples=[["Beach", "Historical"]],
    )

    @field_validator("preferences")
    @classmethod
    def validate_preferences(cls, v):
        valid = {"Beach", "Historical", "Nature", "Adventure", "City"}
        normalized = []
        for pref in v:
            matched = False
            for valid_pref in valid:
                if valid_pref.lower() == pref.strip().lower():
                    normalized.append(valid_pref)
                    matched = True
                    break
            if not matched:
                normalized.append(pref.strip())
        return normalized


class RecommendRequest(BaseModel):
    travelers: List[TravelerInput] = Field(
        ...,
        min_length=1,
        max_length=20,
        description="List of traveler preference inputs",
    )
    budget_per_person: float = Field(
        ...,
        gt=0,
        description="Budget per person in INR",
        examples=[5000],
    )
    accommodation_type: str = Field(
        default="Hotel",
        description="Preferred accommodation type",
        examples=["Hotel"],
    )
    top_n: int = Field(default=5, ge=1, le=10)

    @field_validator("accommodation_type")
    @classmethod
    def validate_accommodation(cls, v):
        valid = {"Hotel", "GuestHouse", "Homestay", "Luxury Camps", "Boutique Hotel", "Resort", "Hostel"}
        if v not in valid:
            return "Hotel"
        return v


# ============================================================
# RESPONSE MODELS
# ============================================================

class TouristSpot(BaseModel):
    name: str
    characteristics: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: Optional[str] = None


class RecommendationItem(BaseModel):
    rank: int
    destination: str
    state: str
    destination_type: str
    description: Optional[str] = None
    group_compatibility: float
    group_preference_match: float
    kmeans_cluster_support: float
    predicted_experience: float
    suitability: float
    average_rating: float
    popularity: float
    sentiment_score: Optional[float] = None
    seasonal_score: Optional[float] = None
    in_peak_season: Optional[bool] = None
    budget_status: str
    budget_fit: float
    predicted_accommodation_cost: Optional[float] = None
    best_time: str
    why_this_destination: str
    tourist_spots: List[TouristSpot] = []
    total_spots: int = 0


class RecommendResponse(BaseModel):
    success: bool
    total_travelers: int
    budget_per_person: float
    accommodation_type: str
    recommendations: List[RecommendationItem]


class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    version: str = "1.0.0"


class AssistantChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None

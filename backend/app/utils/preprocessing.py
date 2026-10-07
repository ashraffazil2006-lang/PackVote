"""
backend/app/utils/preprocessing.py
Utility functions for input preprocessing.
"""
from typing import List


VALID_PREFERENCES = {"Beach", "Historical", "Nature", "Adventure", "City"}
VALID_ACCOMMODATION = {"Hotel", "GuestHouse", "Homestay", "Luxury Camps", "Boutique Hotel", "Resort", "Hostel"}


def normalize_preference(pref: str) -> str:
    """Normalize a single preference string."""
    pref = pref.strip()
    mapping = {
        "beaches": "Beach",
        "beach": "Beach",
        "historical": "Historical",
        "history": "Historical",
        "nature": "Nature",
        "adventure": "Adventure",
        "city": "City",
        "cities": "City",
    }
    return mapping.get(pref.lower(), pref)


def normalize_preferences_list(preferences: List[str]) -> str:
    """Convert a list of preference strings to a comma-separated normalized string."""
    normalized = [normalize_preference(p) for p in preferences]
    return ", ".join(normalized)


def validate_budget(budget: float) -> float:
    """Ensure budget is positive."""
    if budget <= 0:
        raise ValueError("Budget must be greater than 0")
    return budget


def validate_accommodation_type(acc_type: str) -> str:
    """Ensure accommodation type is valid."""
    if acc_type not in VALID_ACCOMMODATION:
        return "Hotel"
    return acc_type

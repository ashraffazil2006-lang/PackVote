"""
backend/app/services/tourist_service.py
Service layer for tourist spot queries.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))

from ml.tourist_spots import (
    load_attractions_table,
    get_tourist_spots_for_destination,
)


def get_spots_for_destination(destination_name: str, max_spots: int = 6) -> list:
    """Get tourist spots for a destination."""
    try:
        attractions = load_attractions_table()
        spots = get_tourist_spots_for_destination(destination_name, attractions, max_spots)
        return spots
    except Exception as e:
        return []

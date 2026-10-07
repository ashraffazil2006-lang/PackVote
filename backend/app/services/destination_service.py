"""
backend/app/services/destination_service.py
Service for comprehensive destination intelligence, trip planning,
tourist attractions, and ML-powered similar destinations.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

from ml.tourist_spots import get_tourist_spots_for_destination, load_tourist_spots_db

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

_intel_cache: Optional[Dict[str, Any]] = None
_tourist_spots_cache = None
_candidates_cache: Optional[pd.DataFrame] = None
_similarity_cache: Optional[pd.DataFrame] = None


def _load_data():
    global _intel_cache, _tourist_spots_cache, _candidates_cache, _similarity_cache
    if _intel_cache is None:
        intel_path = DATA_DIR / "destination_intelligence.json"
        if intel_path.exists():
            with open(intel_path, "r", encoding="utf-8") as f:
                _intel_cache = json.load(f)
        else:
            _intel_cache = {}

    if _tourist_spots_cache is None:
        _tourist_spots_cache = load_tourist_spots_db()

    if _candidates_cache is None:
        cand_path = PROCESSED_DIR / "destination_candidates.csv"
        if cand_path.exists():
            _candidates_cache = pd.read_csv(cand_path)
        else:
            _candidates_cache = pd.DataFrame()

    if _similarity_cache is None:
        sim_path = PROCESSED_DIR / "destination_similarity_matrix.csv"
        if sim_path.exists():
            _similarity_cache = pd.read_csv(sim_path, index_col=0)
        else:
            _similarity_cache = pd.DataFrame()


def find_canonical_name(name_query: str) -> Optional[str]:
    """Fuzzy/case-insensitive match for destination name."""
    _load_data()
    q = name_query.strip().lower()
    
    # 1. Exact match in intelligence
    for dest in _intel_cache.keys():
        if dest.lower() == q:
            return dest
            
    # 2. Substring match
    for dest in _intel_cache.keys():
        if q in dest.lower() or dest.lower() in q:
            return dest

    # 3. Match against candidates
    if not _candidates_cache.empty and "Name" in _candidates_cache.columns:
        for dest in _candidates_cache["Name"].dropna().unique():
            if dest.lower() == q or q in dest.lower() or dest.lower() in q:
                return dest

    return None


def get_all_destinations_summary() -> List[Dict[str, Any]]:
    """Return overview list of all destinations."""
    _load_data()
    results = []
    
    if not _candidates_cache.empty:
        for _, row in _candidates_cache.iterrows():
            name = str(row.get("Name", ""))
            intel = _intel_cache.get(name, {})
            overview = intel.get("overview", {})
            results.append({
                "destination": name,
                "state": str(row.get("State", "")),
                "destination_type": str(row.get("Type", "")),
                "popularity": float(row.get("Popularity", 0)),
                "average_rating": float(row.get("Avg_Rating", 0)),
                "best_time": str(row.get("BestTimeToVisit", "")),
                "tagline": overview.get("tagline", row.get("Description", "")),
                "avg_trip_days": overview.get("avg_trip_days", 4),
            })
    return results


def get_similar_destinations(canonical_name: str, top_n: int = 4) -> List[Dict[str, Any]]:
    """Return top N similar destinations using TF-IDF cosine similarity matrix."""
    _load_data()
    if _similarity_cache.empty or canonical_name not in _similarity_cache.index:
        return []

    try:
        series = _similarity_cache.loc[canonical_name].drop(labels=[canonical_name], errors="ignore")
        top_similar = series.sort_values(ascending=False).head(top_n)
        
        results = []
        for name, score in top_similar.items():
            info = {}
            if not _candidates_cache.empty:
                match = _candidates_cache[_candidates_cache["Name"] == name]
                if not match.empty:
                    row = match.iloc[0]
                    info = {
                        "state": str(row.get("State", "")),
                        "type": str(row.get("Type", "")),
                        "rating": float(row.get("Avg_Rating", 0)),
                        "popularity": float(row.get("Popularity", 0)),
                    }
            results.append({
                "destination": str(name),
                "similarity_score": round(float(score) * 100, 1),
                **info,
            })
        return results
    except Exception as e:
        logger.error(f"Error computing similar destinations for {canonical_name}: {e}")
        return []


def get_destination_full_details(name_query: str) -> Optional[Dict[str, Any]]:
    """Return comprehensive intelligence, timeline, foods, stays, weather, and spots."""
    _load_data()
    canonical = find_canonical_name(name_query)
    if not canonical:
        return None

    intel = _intel_cache.get(canonical, {})
    
    # Candidate row metrics
    candidate_meta = {}
    if not _candidates_cache.empty:
        match = _candidates_cache[_candidates_cache["Name"] == canonical]
        if not match.empty:
            row = match.iloc[0]
            candidate_meta = {
                "destination": canonical,
                "state": str(row.get("State", "")),
                "destination_type": str(row.get("Type", "")),
                "average_rating": float(row.get("Avg_Rating", 0)),
                "popularity": float(row.get("Popularity", 0)),
                "best_time": str(row.get("BestTimeToVisit", "")),
                "cost_average": float(row.get("Cost_Average", 0)) if pd.notna(row.get("Cost_Average")) else None,
                "cost_min": float(row.get("Cost_Min", 0)) if pd.notna(row.get("Cost_Min")) else None,
                "cost_max": float(row.get("Cost_Max", 0)) if pd.notna(row.get("Cost_Max")) else None,
                "description": str(row.get("Description", "")),
            }

    # All tourist spots
    all_spots = get_tourist_spots_for_destination(canonical, _tourist_spots_cache, max_spots=60)
    
    # Similar destinations
    similar = get_similar_destinations(canonical, top_n=4)

    return {
        "destination": canonical,
        "meta": candidate_meta,
        "overview": intel.get("overview", {
            "tagline": candidate_meta.get("description", ""),
            "best_for": ["Groups", "Families", "Travelers"],
            "avg_trip_days": 4,
            "language": "Hindi, English",
        }),
        "how_to_reach": intel.get("how_to_reach", {}),
        "itinerary": intel.get("itinerary", {
            "3_day": [],
            "5_day": [],
        }),
        "food": intel.get("food", []),
        "restaurants": intel.get("restaurants", []),
        "accommodation": intel.get("accommodation", []),
        "weather": intel.get("weather", []),
        "tips": intel.get("tips", []),
        "nearby": intel.get("nearby", []),
        "tourist_spots": all_spots,
        "total_spots": len(all_spots),
        "similar_destinations": similar,
    }

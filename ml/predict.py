"""
ml/predict.py
Inference pipeline entry point.
Accepts raw group input, returns ranked recommendations with ALL tourist spots.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from ml.consensus import get_engine
from ml.ranking import rank_recommendations
from ml.tourist_spots import (
    load_tourist_spots_db,
    load_attractions_table,
    enrich_recommendations_with_spots,
)

# Pre-load tourist spots DB once
_tourist_spots_db = None
_citywise_attractions = None


def _get_tourist_dbs():
    global _tourist_spots_db, _citywise_attractions
    if _tourist_spots_db is None:
        _tourist_spots_db = load_tourist_spots_db()
    if _citywise_attractions is None:
        _citywise_attractions = load_attractions_table()
    return _tourist_spots_db, _citywise_attractions


def get_recommendations(
    group_preferences: list,
    budget_per_person: float,
    accommodation_type: str = "Hotel",
    adults_per_traveler: int = 1,
    children_per_traveler: int = 0,
    top_n: int = 10,
    max_spots: int = 30,
) -> list:
    """
    Full inference pipeline.

    Parameters
    ----------
    group_preferences : list of str
    budget_per_person : float
    accommodation_type : str
    adults_per_traveler : int
    children_per_traveler : int
    top_n : int
    max_spots : int   — max tourist spots per destination (default 30)

    Returns
    -------
    list of dict — ranked recommendations with full tourist spots list
    """
    # Normalize preferences
    normalized_prefs = []
    for pref in group_preferences:
        if isinstance(pref, list):
            normalized_prefs.append(", ".join(pref))
        else:
            normalized_prefs.append(str(pref))

    # Run consensus engine
    engine = get_engine()
    raw_recs = engine.recommend_group(
        group_preferences=normalized_prefs,
        budget_per_person=budget_per_person,
        accommodation_type=accommodation_type,
        adults_per_traveler=adults_per_traveler,
        children_per_traveler=children_per_traveler,
    )

    # Rank + add explanations
    ranked = rank_recommendations(raw_recs)

    # Add ALL tourist spots from Tourist_Spots.csv (by DestinationID)
    tourist_spots_db, citywise_attractions = _get_tourist_dbs()
    ranked = enrich_recommendations_with_spots(
        ranked,
        tourist_spots_db=tourist_spots_db,
        citywise_attractions=citywise_attractions,
        max_spots=max_spots,
    )

    # Take top N
    ranked = ranked.head(top_n)

    # Convert to list of dicts, handle NaN
    result = []
    for _, row in ranked.iterrows():
        record = {}
        for col, val in row.items():
            if col == "Tourist_Spots":
                record[col] = val if isinstance(val, list) else []
            elif hasattr(val, "item"):
                record[col] = val.item() if not pd.isna(val) else None
            elif isinstance(val, float) and pd.isna(val):
                record[col] = None
            else:
                record[col] = val
        result.append(record)

    return result


if __name__ == "__main__":
    prefs = [
        "Beach, Historical",
        "Nature, Adventure",
        "City, Historical",
        "Nature, Adventure",
    ]
    recs = get_recommendations(prefs, budget_per_person=5000)
    for r in recs:
        spots = r.get("Tourist_Spots", [])
        print(f"#{r['Rank']} {r['Destination']} ({r['State']}) — Score: {r['Group_Compatibility']}")
        print(f"   Tourist Spots ({len(spots)} total):")
        for s in spots[:5]:
            print(f"     • {s['name']}  [{s.get('characteristics','')}]")
        if len(spots) > 5:
            print(f"     ... and {len(spots)-5} more")
        print()

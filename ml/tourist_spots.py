"""
ml/tourist_spots.py
Tourist spot integration — fetches verified authentic attractions per destination from Dataset 3.

Key Features:
  - Filters out synthetic placeholders ("View Point 1", "View Point 2", etc.)
  - Cleans concatenated characteristic strings (e.g. "adventureheritagecultural" → ["Adventure", "Heritage", "Cultural"])
  - Generates human-readable addresses and direct Google Maps search URLs
  - Provides entry fees and best times of day
"""
import re
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
DATASETS = BASE / "datasets"
D3 = DATASETS / "3rd" / "Data"
CITYWISE_DIR = D3 / "Citywise Destinations"
PROCESSED_DIR = BASE / "data" / "processed"

# ─── Destination name → DestinationID in Tourist_Spots.csv ───────────────────
DESTINATION_NAME_TO_ID = {
    "Goa Beaches":         1,
    "Goa":                 1,
    "Kovalam Beach":       2,
    "Kovalam":             2,
    "Andaman Islands":     3,
    "Andaman":             3,
    "Radhanagar Beach":    4,
    "Taj Mahal":           5,
    "Agra":                5,
    "Hampi Ruins":         6,
    "Hampi":               6,
    "Ajanta Ellora Caves": 7,
    "Ajanta":              7,
    "Khajuraho Temples":   8,
    "Khajuraho":           8,
    "Kerala Backwaters":   9,
    "Kerala":              9,
    "Coorg":               10,
    "Munnar":              11,
    "Kaziranga":           12,
    "Leh Ladakh":          13,
    "Ladakh":              13,
    "Rishikesh":           14,
    "Manali":              15,
    "Spiti Valley":        16,
    "Spiti":               16,
    "Jaipur City":         17,
    "Jaipur":              17,
    "Varanasi":            18,
    "Mysore":              19,
    "Kolkata":             20,
}

# Real-world locations / states for accurate addresses
DESTINATION_LOCATION_MAP = {
    "Goa Beaches":         "North & South Goa, Goa",
    "Goa":                 "North & South Goa, Goa",
    "Kovalam Beach":       "Thiruvananthapuram, Kerala",
    "Kovalam":             "Thiruvananthapuram, Kerala",
    "Andaman Islands":     "Port Blair & Havelock, Andaman & Nicobar",
    "Andaman":             "Port Blair & Havelock, Andaman & Nicobar",
    "Radhanagar Beach":    "Havelock Island, Andaman & Nicobar",
    "Taj Mahal":           "Agra, Uttar Pradesh",
    "Agra":                "Agra, Uttar Pradesh",
    "Hampi Ruins":         "Hampi, Vijayanagara, Karnataka",
    "Hampi":               "Hampi, Vijayanagara, Karnataka",
    "Ajanta Ellora Caves": "Chhatrapati Sambhajinagar (Aurangabad), Maharashtra",
    "Ajanta":              "Chhatrapati Sambhajinagar (Aurangabad), Maharashtra",
    "Khajuraho Temples":   "Chhatarpur District, Madhya Pradesh",
    "Khajuraho":           "Chhatarpur District, Madhya Pradesh",
    "Kerala Backwaters":   "Alappuzha & Kumarakom, Kerala",
    "Kerala":              "Alappuzha & Kumarakom, Kerala",
    "Coorg":               "Kodagu District, Karnataka",
    "Munnar":              "Idukki District, Kerala",
    "Kaziranga":           "Golaghat & Nagaon, Assam",
    "Leh Ladakh":          "Leh, Ladakh",
    "Ladakh":              "Leh, Ladakh",
    "Rishikesh":           "Dehradun District, Uttarakhand",
    "Manali":              "Kullu District, Himachal Pradesh",
    "Spiti Valley":        "Lahaul and Spiti, Himachal Pradesh",
    "Spiti":               "Lahaul and Spiti, Himachal Pradesh",
    "Jaipur City":         "Jaipur, Rajasthan",
    "Jaipur":              "Jaipur, Rajasthan",
    "Varanasi":            "Varanasi, Uttar Pradesh",
    "Mysore":              "Mysuru, Karnataka",
    "Kolkata":             "Kolkata, West Bengal",
}

# Citywise CSV city-key fallback per destination
DESTINATION_TO_CITY_KEY = {
    "Goa Beaches":         "goa",
    "Goa":                 "goa",
    "Kovalam Beach":       "trivandrum",
    "Kovalam":             "trivandrum",
    "Andaman Islands":     "andaman",
    "Andaman":             "andaman",
    "Radhanagar Beach":    "andaman",
    "Taj Mahal":           "agra",
    "Agra":                "agra",
    "Hampi Ruins":         "hampi",
    "Hampi":               "hampi",
    "Ajanta Ellora Caves": "aurangabad",
    "Ajanta":              "aurangabad",
    "Khajuraho Temples":   "khajuraho",
    "Khajuraho":           "khajuraho",
    "Kerala Backwaters":   "kerala",
    "Kerala":              "kerala",
    "Coorg":               "coorg",
    "Munnar":              "munnar",
    "Kaziranga":           "kaziranga",
    "Leh Ladakh":          "leh",
    "Ladakh":              "leh",
    "Rishikesh":           "rishikesh",
    "Manali":              "manali",
    "Spiti Valley":        "spiti",
    "Spiti":               "spiti",
    "Jaipur City":         "jaipur",
    "Jaipur":              "jaipur",
    "Varanasi":            "varanasi",
    "Mysore":              "mysore",
    "Kolkata":             "kolkata",
}

CITY_ALIASES = {
    "bengaluru": "bangalore",
    "banglore":  "bangalore",
    "calcutta":  "kolkata",
    "bombay":    "mumbai",
}

KNOWN_TAGS = [
    "beach", "nature", "historical", "adventure", "scenic", "heritage",
    "cultural", "temple", "photography", "lake", "mountain", "waterfall",
    "family", "wildlife", "trekking", "fort", "monument", "palace", "spiritual"
]


def clean_characteristics(char_str: Any) -> tuple[str, list]:
    """
    Split comma-separated or concatenated strings (e.g. 'adventureheritagecultural')
    into human-readable tags and a clean comma-separated string.
    """
    if not char_str or pd.isna(char_str):
        return "Sightseeing", ["Sightseeing"]

    s = str(char_str).strip()
    if "," in s:
        tags = [t.strip().title() for t in s.split(",") if t.strip()]
        return ", ".join(tags), tags

    # Search for embedded known tags
    lower_s = s.lower()
    found = []
    for tag in KNOWN_TAGS:
        if tag in lower_s:
            found.append(tag.title())

    if found:
        return ", ".join(found), found
    return s.title(), [s.title()]


# ─── Load Tourist_Spots.csv ───────────────────────────────────────────────────

def load_tourist_spots_db() -> pd.DataFrame:
    """Load Dataset 3 Tourist_Spots.csv with all verified spots."""
    path = D3 / "Tourist_Spots.csv"
    if path.exists():
        df = pd.read_csv(path)
        df["DestinationID"] = pd.to_numeric(df["DestinationID"], errors="coerce")
        for col in ["Latitude", "Longitude"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df["Name"] = df["Name"].fillna("Unknown").astype(str).str.strip()
        df["Characteristics"] = (
            df["Characteristics"].fillna("").astype(str).str.strip()
        )
        if "Entry_Fee" in df.columns:
            df["Entry_Fee"] = pd.to_numeric(df["Entry_Fee"], errors="coerce").fillna(0)
        else:
            df["Entry_Fee"] = 0
        if "Best_Time" in df.columns:
            df["Best_Time"] = df["Best_Time"].fillna("Anytime").astype(str).str.strip()
        else:
            df["Best_Time"] = "Anytime"
        return df

    return pd.DataFrame(
        columns=["DestinationID", "Name", "Latitude", "Longitude", "Characteristics", "Entry_Fee", "Best_Time"]
    )


# ─── Citywise attractions loader ──────────────────────────────────────────────

def normalize_city(city: str) -> str:
    if pd.isna(city):
        return ""
    city = str(city).strip().lower()
    city = re.sub(r"destinations[_\-\s]*", "", city)
    city = re.sub(r"[^a-z0-9\s]", "", city)
    city = re.sub(r"\s+", " ", city).strip()
    return CITY_ALIASES.get(city, city)


def load_citywise_attractions() -> pd.DataFrame:
    """Load all citywise attraction CSV files into one DataFrame."""
    all_rows = []
    if not CITYWISE_DIR.exists():
        return pd.DataFrame(
            columns=["City", "City_Normalized", "Attraction", "Characteristics", "Latitude", "Longitude"]
        )

    for file in sorted(CITYWISE_DIR.glob("*.csv")):
        try:
            df = pd.read_csv(file)
        except Exception:
            continue

        cols_lower = {str(c).strip().lower(): c for c in df.columns}
        name_col  = next((cols_lower[k] for k in ["name", "attraction", "place", "destination"] if k in cols_lower), None)
        char_col  = next((cols_lower[k] for k in ["characteristics", "type", "category", "tags"] if k in cols_lower), None)
        lat_col   = cols_lower.get("latitude") or cols_lower.get("lat")
        lon_col   = cols_lower.get("longitude") or cols_lower.get("lon") or cols_lower.get("lng")

        city_key = normalize_city(file.stem)

        for _, row in df.iterrows():
            attraction      = str(row[name_col]).strip() if name_col and pd.notna(row.get(name_col)) else "Unknown"
            characteristics = str(row[char_col]).strip() if char_col and pd.notna(row.get(char_col)) else ""
            lat = float(row[lat_col]) if lat_col and pd.notna(row.get(lat_col)) else None
            lon = float(row[lon_col]) if lon_col and pd.notna(row.get(lon_col)) else None

            all_rows.append({
                "City":            file.stem.replace("Destinations_", ""),
                "City_Normalized": city_key,
                "Attraction":      attraction,
                "Characteristics": characteristics,
                "Latitude":        lat,
                "Longitude":       lon,
            })

    return pd.DataFrame(all_rows)


# ─── Main spot retrieval ──────────────────────────────────────────────────────

def get_tourist_spots_for_destination(
    destination_name: str,
    tourist_spots_db: pd.DataFrame = None,
    citywise_attractions: pd.DataFrame = None,
    max_spots: int = 30,
) -> list:
    """
    Return authentic, verified tourist spots for a given destination name.

    Filters out synthetic 'View Point N' filler rows from academic dataset
    and enriches with clean addresses and Google Maps links.
    """
    spots = []
    location_str = DESTINATION_LOCATION_MAP.get(destination_name, f"{destination_name}, India")

    # ── 1. Primary: Tourist_Spots.csv ────────────────────────────────────────
    dest_id = DESTINATION_NAME_TO_ID.get(destination_name)

    if dest_id is not None and tourist_spots_db is not None and not tourist_spots_db.empty:
        matched = tourist_spots_db[tourist_spots_db["DestinationID"] == dest_id].copy()
        matched["Name_Clean"] = matched["Name"].str.replace(r"\s*#\d+$", "", regex=True).str.strip()
        matched = matched.drop_duplicates(subset=["Name_Clean"])
        matched = matched[matched["Name_Clean"] != ""].reset_index(drop=True)

        # Filter out generic synthetic placeholders (e.g. 'Goa View Point 1', 'Kerala View Point 42')
        is_synthetic = matched["Name_Clean"].str.contains(r"\bview\s*point\b", case=False, regex=True)
        real_spots = matched[~is_synthetic]
        if not real_spots.empty:
            matched = real_spots.reset_index(drop=True)

        for _, row in matched.iterrows():
            spot_name = row["Name_Clean"]
            clean_str, tags = clean_characteristics(row.get("Characteristics", ""))
            lat = row["Latitude"] if pd.notna(row.get("Latitude")) else None
            lon = row["Longitude"] if pd.notna(row.get("Longitude")) else None
            address = f"{spot_name}, {location_str}"
            maps_query = urllib.parse.quote_plus(f"{spot_name} {location_str}")
            maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
            entry_fee = int(row.get("Entry_Fee", 0)) if pd.notna(row.get("Entry_Fee")) else 0
            best_time = str(row.get("Best_Time", "Anytime")) if pd.notna(row.get("Best_Time")) else "Anytime"

            spots.append({
                "name":            spot_name,
                "characteristics": clean_str,
                "tags":            tags,
                "latitude":        lat,
                "longitude":       lon,
                "address":         address,
                "maps_url":        maps_url,
                "entry_fee":       entry_fee,
                "best_time":       best_time,
                "source":          "Tourist_Spots",
            })
            if len(spots) >= max_spots:
                break

    # ── 2. Fallback: citywise attractions ─────────────────────────────────────
    if not spots and citywise_attractions is not None and not citywise_attractions.empty:
        city_key = DESTINATION_TO_CITY_KEY.get(destination_name, "")
        if city_key:
            matched = citywise_attractions[
                citywise_attractions["City_Normalized"].str.contains(city_key, na=False)
            ].copy()
            # Filter synthetic view points here as well
            is_synthetic = matched["Attraction"].str.contains(r"\bview\s*point\b", case=False, regex=True)
            real_matched = matched[~is_synthetic]
            if not real_matched.empty:
                matched = real_matched

            for _, row in matched.head(max_spots).iterrows():
                spot_name = row.get("Attraction", "Unknown")
                clean_str, tags = clean_characteristics(row.get("Characteristics", ""))
                lat = row.get("Latitude")
                lon = row.get("Longitude")
                address = f"{spot_name}, {location_str}"
                maps_query = urllib.parse.quote_plus(f"{spot_name} {location_str}")
                maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"

                spots.append({
                    "name":            spot_name,
                    "characteristics": clean_str,
                    "tags":            tags,
                    "latitude":        lat,
                    "longitude":       lon,
                    "address":         address,
                    "maps_url":        maps_url,
                    "entry_fee":       0,
                    "best_time":       "Anytime",
                    "source":          "Citywise",
                })

    return spots


# ─── Enrich recommendations ───────────────────────────────────────────────────

def enrich_recommendations_with_spots(
    recommendations: pd.DataFrame,
    tourist_spots_db: pd.DataFrame = None,
    citywise_attractions: pd.DataFrame = None,
    max_spots: int = 30,
) -> pd.DataFrame:
    """Add Tourist_Spots list column to each recommendation row."""
    if tourist_spots_db is None:
        tourist_spots_db = load_tourist_spots_db()
    if citywise_attractions is None:
        citywise_attractions = load_citywise_attractions()

    recommendations = recommendations.copy()
    spots_col = []
    for _, row in recommendations.iterrows():
        spots = get_tourist_spots_for_destination(
            destination_name=row["Destination"],
            tourist_spots_db=tourist_spots_db,
            citywise_attractions=citywise_attractions,
            max_spots=max_spots,
        )
        spots_col.append(spots)
    recommendations["Tourist_Spots"] = spots_col
    return recommendations


# ─── Persistence ─────────────────────────────────────────────────────────────

def save_attractions_table(df: pd.DataFrame):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DIR / "packvote_citywise_attractions.csv", index=False)


def load_attractions_table() -> pd.DataFrame:
    path = PROCESSED_DIR / "packvote_citywise_attractions.csv"
    if path.exists():
        return pd.read_csv(path)
    return load_citywise_attractions()

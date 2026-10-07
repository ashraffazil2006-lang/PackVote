"""
ml/preprocessing.py
Data loading and cleaning — faithful to the notebook.
"""
import re
import csv
import numpy as np
import pandas as pd
from pathlib import Path


# ============================================================
# Paths
# ============================================================

BASE = Path(__file__).resolve().parent.parent
DATASETS = BASE / "datasets"
D1 = DATASETS / "1st"
D2 = DATASETS / "2nd"
D3 = DATASETS / "3rd" / "Data"
PROCESSED = BASE / "data" / "processed"


# ============================================================
# Raw data loaders
# ============================================================

def load_raw_datasets():
    """Load all raw datasets and return as dict."""
    users = pd.read_csv(D1 / "Final_Updated_Expanded_Users.csv")
    destinations = pd.read_csv(D1 / "Expanded_Destinations.csv")
    reviews = pd.read_csv(D1 / "Final_Updated_Expanded_Reviews.csv")
    user_history = pd.read_csv(D1 / "Final_Updated_Expanded_UserHistory.csv")
    travel_cost = pd.read_csv(D2 / "travel cost.csv")
    tourist_spots = pd.read_csv(D3 / "Tourist_Spots.csv")
    characteristics = pd.read_csv(D3 / "Characteristics.csv")

    return {
        "users": users,
        "destinations": destinations,
        "reviews": reviews,
        "user_history": user_history,
        "travel_cost": travel_cost,
        "tourist_spots": tourist_spots,
        "characteristics": characteristics,
    }


def read_user_visits(path=None):
    """Read semicolon-delimited User_Visits.csv (Dataset 3)."""
    if path is None:
        path = D3 / "User_Visits.csv"
    rows = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]
            line = line.replace('""', '"')
            row = next(csv.reader([line], delimiter=";"))
            rows.append(row)
    return pd.DataFrame(rows[1:], columns=rows[0])


# ============================================================
# Cleaning helpers
# ============================================================

def clean_column_names(df):
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace(" ", "_", regex=False)
    )
    return df


def clean_text_columns(df):
    df = df.copy()
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )
        df[col] = df[col].replace(["", "nan", "None", "NULL", "null"], np.nan)
    return df


def normalize_preferences(text):
    """Standardize preference strings to consistent categories."""
    text = str(text).lower().strip()
    mapping = {
        "beaches": "Beach",
        "beach": "Beach",
        "historical": "Historical",
        "history": "Historical",
        "nature": "Nature",
        "adventure": "Adventure",
        "city": "City",
    }
    parts = [p.strip() for p in text.split(",")]
    normalized = []
    for part in parts:
        if part in mapping:
            normalized.append(mapping[part])
    normalized = list(dict.fromkeys(normalized))
    return ", ".join(normalized) if normalized else "Unknown"


def parse_cost(value):
    """Parse accommodation cost range string to (min, max, avg, flag)."""
    if pd.isna(value):
        return np.nan, np.nan, np.nan, "MISSING"
    text = str(value).strip()
    numbers = re.findall(r"\d+(?:\.\d+)?", text)
    if len(numbers) == 0:
        return np.nan, np.nan, np.nan, "INVALID"
    if len(numbers) == 1:
        v = float(numbers[0])
        return v, v, v, "SINGLE_VALUE"
    v1, v2 = float(numbers[0]), float(numbers[1])
    if v1 > v2:
        return v2, v1, (v1 + v2) / 2, "INVERTED_CORRECTED"
    return v1, v2, (v1 + v2) / 2, "VALID"


# ============================================================
# Full preprocessing pipeline
# ============================================================

def preprocess_all(save=True):
    """
    Load → clean → feature-engineer all datasets.
    Returns dict of processed DataFrames.
    """
    raw = load_raw_datasets()

    # Working copies
    users_p = raw["users"].copy()
    destinations_p = raw["destinations"].copy()
    reviews_p = raw["reviews"].copy()
    user_history_p = raw["user_history"].copy()
    travel_cost_p = raw["travel_cost"].copy()
    tourist_spots_p = raw["tourist_spots"].copy()
    characteristics_p = raw["characteristics"].copy()

    # Clean column names and text
    for name, df in [
        ("users_p", users_p),
        ("destinations_p", destinations_p),
        ("reviews_p", reviews_p),
        ("user_history_p", user_history_p),
        ("travel_cost_p", travel_cost_p),
        ("tourist_spots_p", tourist_spots_p),
        ("characteristics_p", characteristics_p),
    ]:
        locals()[name] = clean_text_columns(clean_column_names(df))

    # Re-assign after loop (Python scope)
    users_p = clean_text_columns(clean_column_names(users_p))
    destinations_p = clean_text_columns(clean_column_names(destinations_p))
    reviews_p = clean_text_columns(clean_column_names(reviews_p))
    user_history_p = clean_text_columns(clean_column_names(user_history_p))
    travel_cost_p = clean_text_columns(clean_column_names(travel_cost_p))
    tourist_spots_p = clean_text_columns(clean_column_names(tourist_spots_p))
    characteristics_p = clean_text_columns(clean_column_names(characteristics_p))

    # --- USERS ---
    users_p["Preferences"] = users_p["Preferences"].fillna("Unknown")
    users_p["Preferences_Clean"] = users_p["Preferences"].apply(normalize_preferences)
    for col in ["NumberOfAdults", "NumberOfChildren"]:
        users_p[col] = pd.to_numeric(users_p[col], errors="coerce")
        users_p[col] = users_p[col].fillna(users_p[col].median())

    PREFERENCE_CATEGORIES = ["Beach", "Historical", "Nature", "Adventure", "City"]
    for category in PREFERENCE_CATEGORIES:
        users_p[f"Pref_{category}"] = (
            users_p["Preferences_Clean"]
            .str.contains(category, case=False, na=False)
            .astype(int)
        )

    # --- DESTINATIONS ---
    destinations_p["DestinationID"] = pd.to_numeric(destinations_p["DestinationID"], errors="coerce")
    destinations_p["Popularity"] = pd.to_numeric(destinations_p["Popularity"], errors="coerce")
    for col in ["Name", "State", "Type", "BestTimeToVisit"]:
        destinations_p[col] = destinations_p[col].fillna("Unknown")
    destinations_p = destinations_p.drop_duplicates()

    # --- REVIEWS ---
    reviews_p["Rating"] = pd.to_numeric(reviews_p["Rating"], errors="coerce")
    reviews_p["ReviewText"] = (
        reviews_p["ReviewText"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.replace(r"[^a-zA-Z0-9\s]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    reviews_p["Invalid_Rating"] = (reviews_p["Rating"] < 1) | (reviews_p["Rating"] > 5)
    reviews_ml = reviews_p[reviews_p["Rating"].between(1, 5)].copy()

    # --- USER HISTORY ---
    for col in ["HistoryID", "UserID", "DestinationID", "ExperienceRating"]:
        user_history_p[col] = pd.to_numeric(user_history_p[col], errors="coerce")
    user_history_p["VisitDate"] = pd.to_datetime(user_history_p["VisitDate"], errors="coerce")

    # --- TRAVEL COST ---
    parsed = travel_cost_p["Accomdation_Cost"].apply(parse_cost)
    travel_cost_p[["Cost_Min", "Cost_Max", "Cost_Average", "Cost_Flag"]] = pd.DataFrame(
        parsed.tolist(), index=travel_cost_p.index
    )

    # --- TOURIST SPOTS ---
    tourist_spots_p["DestinationID"] = pd.to_numeric(tourist_spots_p["DestinationID"], errors="coerce")
    for col in ["Latitude", "Longitude"]:
        tourist_spots_p[col] = pd.to_numeric(tourist_spots_p[col], errors="coerce")
    tourist_spots_p["Name"] = tourist_spots_p["Name"].fillna("Unknown")
    tourist_spots_p["Characteristics"] = (
        tourist_spots_p["Characteristics"]
        .fillna("Unknown")
        .astype(str)
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    tourist_spots_p = tourist_spots_p.drop_duplicates()

    # --- CHARACTERISTICS ---
    characteristics_p["characteristics"] = (
        characteristics_p["characteristics"]
        .fillna("Unknown")
        .astype(str)
        .str.lower()
        .str.strip()
    )
    characteristics_p = characteristics_p.drop_duplicates()

    # --- USER VISITS ---
    try:
        user_visits_p = read_user_visits()
        for col in ["photoID", "userID", "poiID", "poiFreq", "seqID"]:
            if col in user_visits_p.columns:
                user_visits_p[col] = pd.to_numeric(user_visits_p[col], errors="coerce")
        if "dateTaken" in user_visits_p.columns:
            user_visits_p["dateTaken"] = pd.to_datetime(user_visits_p["dateTaken"], errors="coerce")
    except Exception as e:
        print(f"Warning: could not load User_Visits: {e}")
        user_visits_p = pd.DataFrame()

    result = {
        "users_p": users_p,
        "destinations_p": destinations_p,
        "reviews_p": reviews_p,
        "reviews_ml": reviews_ml,
        "user_history_p": user_history_p,
        "travel_cost_p": travel_cost_p,
        "tourist_spots_p": tourist_spots_p,
        "characteristics_p": characteristics_p,
        "user_visits_p": user_visits_p,
    }

    if save:
        PROCESSED.mkdir(parents=True, exist_ok=True)
        users_p.to_csv(PROCESSED / "users_processed.csv", index=False)
        destinations_p.to_csv(PROCESSED / "destinations_processed.csv", index=False)
        reviews_p.to_csv(PROCESSED / "reviews_processed.csv", index=False)
        reviews_ml.to_csv(PROCESSED / "reviews_ml.csv", index=False)
        user_history_p.to_csv(PROCESSED / "user_history_processed.csv", index=False)
        travel_cost_p.to_csv(PROCESSED / "travel_cost_processed.csv", index=False)
        tourist_spots_p.to_csv(PROCESSED / "tourist_spots_processed.csv", index=False)
        characteristics_p.to_csv(PROCESSED / "characteristics_processed.csv", index=False)

    return result


if __name__ == "__main__":
    data = preprocess_all(save=True)
    for name, df in data.items():
        print(f"{name:30s}: {df.shape}")

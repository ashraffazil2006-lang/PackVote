# PACKVOTE — Project Analysis

## 1. Project Overview

**PACKVOTE** is a Machine Learning-based Group Travel Recommendation and Budget-Aware Destination Planning System. It accepts individual traveler preferences from multiple group members, runs them through a consensus-based ML pipeline, and returns ranked travel destinations that maximize collective satisfaction while respecting budget constraints.

---

## 2. Architecture

```
PACKVOTE/
├── datasets/          ← Recreated synthetic datasets (3 datasets)
├── data/processed/    ← Cleaned CSVs + model_metrics.json
├── models/            ← Trained .pkl model artifacts (11 files)
├── ml/                ← ML pipeline modules
│   ├── preprocessing.py   Data loading + cleaning
│   ├── features.py        Feature engineering
│   ├── models.py          Train/save/load all 5 models
│   ├── consensus.py       Group Consensus Engine
│   ├── ranking.py         Ranking + explanation generation
│   ├── tourist_spots.py   Attraction enrichment
│   ├── train_models.py    One-shot training script
│   └── predict.py         Inference entry point
├── backend/           ← FastAPI REST API
│   └── app/
│       ├── main.py        FastAPI app + CORS + routes
│       ├── schemas.py     Pydantic request/response models
│       └── services/      Business logic layer
└── frontend/          ← React + Vite
    └── src/
        ├── components/    Header, TravelerInput, BudgetInput,
        │                  RecommendationCard, RecommendationList,
        │                  TouristSpotList, Loading
        ├── pages/         Home page
        ├── services/      api.js (fetch wrapper)
        └── App.jsx
```

---

## 3. Datasets

| Dataset | File | Rows | Description |
|---------|------|------|-------------|
| D1 Users | `datasets/1st/Final_Updated_Expanded_Users.csv` | 999 | UserID, Name, Email, Preferences, Gender, Adults, Children |
| D1 Destinations | `datasets/1st/Expanded_Destinations.csv` | 1000 | DestinationID, Name, State, Type, Popularity, BestTimeToVisit |
| D1 Reviews | `datasets/1st/Final_Updated_Expanded_Reviews.csv` | 999 | ReviewID, DestinationID, UserID, Rating (1-5), ReviewText |
| D1 UserHistory | `datasets/1st/Final_Updated_Expanded_UserHistory.csv` | 999 | HistoryID, UserID, DestinationID, VisitDate, ExperienceRating |
| D2 Travel Cost | `datasets/2nd/travel cost.csv` | 500 | City, Accomadation_Type, Accomdation_Cost (range string) |
| D3 Tourist Spots | `datasets/3rd/Data/Tourist_Spots.csv` | 459 | DestinationID, Name, Latitude, Longitude, Characteristics |
| D3 Characteristics | `datasets/3rd/Data/Characteristics.csv` | 131 | characteristics |
| D3 User Visits | `datasets/3rd/Data/User_Visits.csv` | 34515 | photoID;userID;poiID;poiFreq;dateTaken;seqID (semicolon-delimited) |
| D3 Citywise | `datasets/3rd/Data/Citywise Destinations/*.csv` | 13 cities | Name, Characteristics, Latitude, Longitude |

**Destinations in scope:** Taj Mahal (Historical), Goa Beaches (Beach), Jaipur City (City), Kerala Backwaters (Nature), Leh Ladakh (Adventure).

---

## 4. ML Pipeline

### 4.1 K-Means — Traveler Profiling
- **Input:** User preference flags + group size + experience history
- **Output:** Cluster ID per traveler (4 clusters)
- **Role:** Provides cluster-level preference profiles for the consensus engine
- **Training metric:** Inertia = 8895.26

### 4.2 KNN — Experience Prediction
- **Input:** Traveler preferences × destination type × popularity × group size
- **NO target leakage:** ExperienceRating is the *target*, never an input
- **Output:** Predicted experience rating (1–5)
- **Best K:** Selected by lowest MAE across k ∈ {3, 5, 7, 9, 11}

### 4.3 Decision Tree — Destination Suitability
- **Input:** Same feature set as KNN
- **Output:** Suitability probability (0–1)
- **Target:** `Suitable = 1` if ExperienceRating ≥ 4
- **Class balancing:** `class_weight="balanced"`

### 4.4 Naive Bayes — Review Sentiment
- **Input:** TF-IDF (max 1000 features, bigrams) of ReviewText
- **Output:** Positive (1) / Negative (0) label
- **Role:** Helps understand destination reputation from textual reviews

### 4.5 Linear Regression — Accommodation Cost
- **Input:** City + AccommodationType (one-hot encoded via Pipeline)
- **Output:** Predicted nightly cost in INR
- **R²:** 0.9499 (high fit due to consistent price ranges per city/type)

### 4.6 Group Consensus Engine
The scoring layer (NOT an ML model) combining all outputs:

```
Individual score per traveler =
    0.30 × preference_match
  + 0.20 × experience_score        (KNN output, normalized 0-1)
  + 0.20 × suitability_probability (Decision Tree output)
  + 0.10 × rating_norm             (Avg review rating / 5)
  + 0.10 × popularity_norm         (normalized popularity)
  + 0.10 × cluster_support         (K-Means cluster alignment)

Final Group Score =
    0.70 × average_member_score
  + 0.15 × minimum_member_score    (least-satisfied traveler)
  + 0.15 × budget_fit × 100
```

---

## 5. API Reference

### `GET /api/health`
Returns backend and model status.

### `POST /api/recommend`
**Request:**
```json
{
  "travelers": [
    {"preferences": ["Beach", "Historical"]},
    {"preferences": ["Nature", "Adventure"]}
  ],
  "budget_per_person": 5000,
  "accommodation_type": "Hotel",
  "top_n": 5
}
```

**Response:**
```json
{
  "success": true,
  "total_travelers": 2,
  "recommendations": [
    {
      "rank": 1,
      "destination": "Goa Beaches",
      "state": "Goa",
      "destination_type": "Beach",
      "group_compatibility": 54.84,
      "group_preference_match": 50.0,
      "kmeans_cluster_support": 42.5,
      "predicted_experience": 3.47,
      "suitability": 65.2,
      "average_rating": 3.12,
      "popularity": 8.6,
      "budget_status": "Within budget",
      "budget_fit": 100.0,
      "predicted_accommodation_cost": 4200.0,
      "best_time": "Nov-Mar",
      "why_this_destination": "This destination was selected because of: good match with the group's preferences, moderate destination suitability, fits within the group's budget.",
      "tourist_spots": [
        {"name": "Baga Beach", "characteristics": "beach, scenic", "latitude": 15.55, "longitude": 73.75}
      ]
    }
  ]
}
```

---

## 6. Data Integrity Constraints

| Constraint | Implementation |
|------------|----------------|
| No target leakage | `ExperienceRating` never appears in KNN input features |
| No fabricated metrics | All metrics computed from actual model outputs |
| Budget neutrality | Destinations without cost data get `budget_fit = 0.5` (neutral) |
| Rating validity | Only reviews with `Rating ∈ [1,5]` are used for training |
| Class balance | Decision Tree uses `class_weight="balanced"` |
| Cost parsing | Handles ranges like "1500 - 8000", inverted ranges, single values |

---

## 7. Model Metrics

| Model | Key Metrics |
|-------|-------------|
| K-Means | k=4, Inertia=8895.26 |
| KNN | Best k=11, MAE=1.32, R²=-0.11 (random-data baseline) |
| Decision Tree | depth=4, Acc=0.535, F1=0.518 |
| Naive Bayes | alpha=0.1, Acc=0.59, F1=0.128 |
| Linear Regression | MAE=₹768, R²=0.95 |

> [!NOTE]
> KNN and Decision Tree metrics are lower because the synthetic dataset uses random experience ratings, not real user data. These would improve significantly with real PACKVOTE survey data.

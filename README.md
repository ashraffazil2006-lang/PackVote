# PACKVOTE — ML-Based Group Travel Recommendation System

> **An end-to-end full-stack application**: ML pipeline → FastAPI backend → React frontend

---

## What is PACKVOTE?

PACKVOTE takes individual travel preferences from each member of a group, runs them through a **multi-model ML consensus engine**, and returns ranked destination recommendations that balance everyone's preferences against a shared accommodation budget.

### ML Models Used
| Model | Role |
|-------|------|
| **K-Means** | Cluster travelers into profiles |
| **KNN** | Predict per-traveler experience score at each destination |
| **Decision Tree** | Predict destination suitability probability |
| **Naive Bayes** | Classify review sentiment (TF-IDF) |
| **Linear Regression** | Predict nightly accommodation cost |

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Install Python dependencies

```powershell
pip install scikit-learn pandas numpy joblib fastapi uvicorn[standard] pydantic
```

### 2. Train the ML models (one-time)

```powershell
cd d:\PACKVOTE
python ml/train_models.py
```

Output: All 5 models saved to `models/`, processed CSVs to `data/processed/`.

### 3. Start the backend

```powershell
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

API docs available at: **http://localhost:8000/api/docs**

### 4. Start the frontend

```powershell
cd frontend
npm install
npm run dev
```

App available at: **http://localhost:5173**

---

## Running Tests

```powershell
# ML unit tests (no server needed)
python -m pytest tests/test_ml.py -v

# Backend integration tests (server must be running)
python -m pytest tests/test_backend.py -v
```

---

## Project Structure

```
PACKVOTE/
├── datasets/               ← Raw datasets (3 sources)
├── data/processed/         ← Cleaned CSVs + metrics JSON
├── models/                 ← Trained .pkl model artifacts
├── ml/                     ← ML pipeline (Python modules)
├── backend/                ← FastAPI REST API
├── frontend/               ← React + Vite UI
├── tests/                  ← Unit + integration tests
├── PROJECT_ANALYSIS.md     ← Full technical analysis
└── RUN_GUIDE.md            ← Step-by-step run instructions
```

---

## API

`POST http://localhost:8000/api/recommend`

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

See full API docs at `/api/docs`.

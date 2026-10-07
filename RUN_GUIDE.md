# PACKVOTE — Run Guide

## Step-by-Step Instructions

---

## Terminal 1 — Backend

```powershell
# From the project root
cd d:\PACKVOTE

# (First time only) Train all ML models
python ml/train_models.py

# Start the FastAPI server
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

**Verify:**
- http://localhost:8000/api/health → `{"status":"ok","models_loaded":true}`
- http://localhost:8000/api/docs → Interactive Swagger UI

---

## Terminal 2 — Frontend

```powershell
cd d:\PACKVOTE\frontend
npm install       # first time only
npm run dev
```

**Open:** http://localhost:5173

---

## Terminal 3 — Tests (optional)

```powershell
cd d:\PACKVOTE

# ML unit tests (no server needed)
python -m pytest tests/test_ml.py -v

# Backend integration tests (backend must be running)
python -m pytest tests/test_backend.py -v

# All tests
python -m pytest tests/ -v
```

---

## Troubleshooting

### "ML models not found"
Run `python ml/train_models.py` first.

### Frontend shows "Backend Unavailable"
Make sure the backend is running on port 8000.

### CORS errors in browser
The backend allows all origins by default (`allow_origins=["*"]`). No action needed for local dev.

### Pandas deprecation warnings
Informational only, do not affect functionality.

---

## Retrain Models

To retrain from scratch (e.g., after changing dataset or features):

```powershell
# Delete existing models (optional)
Remove-Item d:\PACKVOTE\models\*.pkl

# Retrain
python ml/train_models.py
```

---

## API Reference (Quick)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Check backend + model status |
| POST | `/api/recommend` | Get group travel recommendations |
| GET | `/api/docs` | Swagger UI |
| GET | `/api/redoc` | ReDoc UI |

### Valid Preferences
`Beach`, `Historical`, `Nature`, `Adventure`, `City`

### Valid Accommodation Types
`Hotel`, `GuestHouse`, `Homestay`, `Luxury Camps`, `Boutique Hotel`, `Resort`, `Hostel`

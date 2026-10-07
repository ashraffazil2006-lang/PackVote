"""
backend/app/main.py
FastAPI application — PACKVOTE Backend.
"""
import sys
import logging
from pathlib import Path

# Add project root to Python path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.schemas import (
    RecommendRequest,
    RecommendResponse,
    HealthResponse,
    AssistantChatRequest,
)
from backend.app.services.recommendation_service import build_recommendations
from backend.app.services.ml_service import get_ml_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# FastAPI app
# ============================================================

app = FastAPI(
    title="PACKVOTE API",
    description=(
        "ML-Based Group Travel Recommendation and "
        "Budget-Aware Destination Planning System"
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Startup: pre-load models
# ============================================================

@app.on_event("startup")
async def startup_event():
    logger.info("PACKVOTE backend starting up...")
    try:
        svc = get_ml_service()
        svc.ensure_loaded()
        logger.info("ML models loaded successfully.")
    except Exception as e:
        logger.warning(f"Could not pre-load models: {e}")


# ============================================================
# Routes
# ============================================================

@app.get("/api/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check backend and model status."""
    svc = get_ml_service()
    return HealthResponse(
        status="ok",
        models_loaded=svc.is_loaded,
    )


@app.post("/api/recommend", response_model=RecommendResponse, tags=["Recommendations"])
async def recommend(request: RecommendRequest):
    """
    Get group travel recommendations based on traveler preferences and budget.

    **Request body:**
    - `travelers`: list of traveler objects with `preferences` (list of strings)
    - `budget_per_person`: accommodation budget per person in INR
    - `accommodation_type`: one of Hotel, GuestHouse, Homestay, Luxury Camps, Boutique Hotel, Resort, Hostel
    - `top_n`: number of recommendations to return (1-10, default 5)

    **Response:**
    - Ranked list of destinations with compatibility scores, budget fit, tourist spots, etc.
    """
    try:
        if not request.travelers:
            raise HTTPException(status_code=400, detail="At least one traveler is required.")

        # Validate all travelers have preferences
        for i, traveler in enumerate(request.travelers):
            if not traveler.preferences:
                raise HTTPException(
                    status_code=400,
                    detail=f"Traveler {i+1} has no preferences specified.",
                )

        recommendations = build_recommendations(
            travelers=request.travelers,
            budget_per_person=request.budget_per_person,
            accommodation_type=request.accommodation_type,
            top_n=request.top_n,
        )

        return RecommendResponse(
            success=True,
            total_travelers=len(request.travelers),
            budget_per_person=request.budget_per_person,
            accommodation_type=request.accommodation_type,
            recommendations=recommendations,
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.exception("Unexpected error in /api/recommend")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/destinations", tags=["Destinations"])
async def list_destinations():
    """Get list and overview of all 20 destinations supported by PACKVOTE."""
    from backend.app.services.destination_service import get_all_destinations_summary
    return {
        "success": True,
        "count": len(get_all_destinations_summary()),
        "destinations": get_all_destinations_summary(),
    }


@app.get("/api/destination/{name}", tags=["Destinations"])
async def get_destination_details(name: str):
    """
    Get full trip details for any destination (e.g., 'Kerala Backwaters', 'Goa', etc.).
    Returns timeline/itinerary, must-try food, restaurants, stays, monthly weather,
    all tourist spots, travel tips, and similar destinations.
    """
    from backend.app.services.destination_service import get_destination_full_details
    details = get_destination_full_details(name)
    if not details:
        raise HTTPException(status_code=404, detail=f"Destination '{name}' not found.")
    return {
        "success": True,
        "data": details,
    }


@app.get("/api/destination/{name}/similar", tags=["Destinations"])
async def get_similar(name: str):
    """Get similar destinations computed using TF-IDF Cosine Similarity."""
    from backend.app.services.destination_service import find_canonical_name, get_similar_destinations
    canonical = find_canonical_name(name)
    if not canonical:
        raise HTTPException(status_code=404, detail=f"Destination '{name}' not found.")
    similar = get_similar_destinations(canonical, top_n=4)
    return {
        "success": True,
        "destination": canonical,
        "similar": similar,
    }


@app.get("/api/analytics", tags=["Analytics"])
async def get_analytics():
    """Get ML evaluation benchmarks, K-Means clustering analysis, and multi-model prediction curve data."""
    from backend.app.services.analytics_service import get_ml_analytics_data
    return {
        "success": True,
        "data": get_ml_analytics_data()
    }


@app.post("/api/assistant/chat", tags=["Assistant"])
async def assistant_chat(request: AssistantChatRequest):
    """AI Voice Assistant chat endpoint for speech and text interaction."""
    from backend.app.services.assistant_service import process_assistant_message
    result = process_assistant_message(request.message, request.context)
    return {
        "success": True,
        "data": result,
    }



DIST_DIR = ROOT / "frontend" / "dist"
if DIST_DIR.exists():
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="static")
else:
    @app.get("/", tags=["System"])
    async def root():
        return {
            "message": "PACKVOTE API",
            "version": "1.0.0",
            "docs": "/api/docs",
        }

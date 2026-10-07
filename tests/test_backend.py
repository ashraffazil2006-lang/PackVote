"""
tests/test_backend.py
Integration tests for the PACKVOTE FastAPI backend.
Run with the server live: python -m uvicorn backend.app.main:app --port 8000
"""
import sys
import json
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

BASE_URL = "http://localhost:8000"


def _get(path):
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=10) as r:
        return json.loads(r.read()), r.status


def _post(path, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code


# ============================================================
# Health check
# ============================================================

def test_health_ok():
    resp, status = _get("/api/health")
    assert status == 200
    assert resp["status"] == "ok"

def test_health_models_loaded():
    resp, status = _get("/api/health")
    assert resp["models_loaded"] is True

def test_root_ok():
    with urllib.request.urlopen(f"{BASE_URL}/", timeout=10) as r:
        assert r.status == 200
        content = r.read().decode("utf-8", errors="ignore")
        assert "PACKVOTE" in content or "packvote" in content.lower()


def test_assistant_chat_ok():
    resp, status = _post("/api/assistant/chat", {"message": "Plan a beach trip for 2"})
    assert status == 200
    assert resp["success"] is True
    assert "reply" in resp["data"]
    assert "action" in resp["data"]



# ============================================================
# Recommend endpoint
# ============================================================

SAMPLE_PAYLOAD = {
    "travelers": [
        {"preferences": ["Beach", "Historical"]},
        {"preferences": ["Nature", "Adventure"]},
    ],
    "budget_per_person": 5000,
    "accommodation_type": "Hotel",
    "top_n": 5,
}

def test_recommend_success():
    resp, status = _post("/api/recommend", SAMPLE_PAYLOAD)
    assert status == 200
    assert resp["success"] is True

def test_recommend_returns_correct_count():
    resp, status = _post("/api/recommend", SAMPLE_PAYLOAD)
    assert len(resp["recommendations"]) <= 5

def test_recommend_travelers_count():
    resp, status = _post("/api/recommend", SAMPLE_PAYLOAD)
    assert resp["total_travelers"] == 2

def test_recommend_echoes_budget():
    resp, status = _post("/api/recommend", SAMPLE_PAYLOAD)
    assert resp["budget_per_person"] == 5000

def test_recommend_ranks_ordered():
    resp, status = _post("/api/recommend", SAMPLE_PAYLOAD)
    ranks = [r["rank"] for r in resp["recommendations"]]
    assert ranks == sorted(ranks)

def test_recommend_scores_bounded():
    resp, status = _post("/api/recommend", SAMPLE_PAYLOAD)
    for r in resp["recommendations"]:
        assert 0 <= r["group_compatibility"] <= 100
        assert 1 <= r["predicted_experience"] <= 5

def test_recommend_has_explanation():
    resp, status = _post("/api/recommend", SAMPLE_PAYLOAD)
    for r in resp["recommendations"]:
        assert isinstance(r["why_this_destination"], str)
        assert len(r["why_this_destination"]) > 5

def test_recommend_budget_status_valid():
    resp, status = _post("/api/recommend", SAMPLE_PAYLOAD)
    valid = {"Within budget", "Above budget", "Cost data unavailable", "Cost prediction unavailable"}
    for r in resp["recommendations"]:
        assert r["budget_status"] in valid

def test_recommend_different_preferences():
    payload = {
        "travelers": [{"preferences": ["City"]}],
        "budget_per_person": 10000,
        "accommodation_type": "Resort",
        "top_n": 3,
    }
    resp, status = _post("/api/recommend", payload)
    assert status == 200
    assert len(resp["recommendations"]) > 0

def test_recommend_single_traveler():
    payload = {
        "travelers": [{"preferences": ["Nature"]}],
        "budget_per_person": 2000,
        "accommodation_type": "Hostel",
        "top_n": 5,
    }
    resp, status = _post("/api/recommend", payload)
    assert status == 200
    assert resp["total_travelers"] == 1

def test_recommend_many_travelers():
    payload = {
        "travelers": [{"preferences": ["Beach"]}] * 8,
        "budget_per_person": 5000,
        "accommodation_type": "Hotel",
        "top_n": 5,
    }
    resp, status = _post("/api/recommend", payload)
    assert status == 200

# ─── Validation errors ───

def test_recommend_empty_travelers_fails():
    payload = {**SAMPLE_PAYLOAD, "travelers": []}
    resp, status = _post("/api/recommend", payload)
    assert status in (400, 422)

def test_recommend_no_preferences_fails():
    payload = {**SAMPLE_PAYLOAD, "travelers": [{"preferences": []}]}
    resp, status = _post("/api/recommend", payload)
    assert status in (400, 422)

def test_recommend_negative_budget_fails():
    payload = {**SAMPLE_PAYLOAD, "budget_per_person": -100}
    resp, status = _post("/api/recommend", payload)
    assert status == 422

def test_recommend_invalid_topn_fails():
    payload = {**SAMPLE_PAYLOAD, "top_n": 50}
    resp, status = _post("/api/recommend", payload)
    assert status == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

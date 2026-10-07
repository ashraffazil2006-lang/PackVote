"""
tests/test_ml.py
Unit tests for the PACKVOTE ML pipeline.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
import pandas as pd
import numpy as np


# ============================================================
# Preprocessing tests
# ============================================================

def test_preprocess_runs():
    from ml.preprocessing import preprocess_all
    data = preprocess_all(save=False)
    assert 'users_p' in data
    assert 'destinations_p' in data
    assert 'reviews_ml' in data
    assert len(data['users_p']) > 0
    assert len(data['destinations_p']) > 0

def test_users_have_preference_cols():
    from ml.preprocessing import preprocess_all
    data = preprocess_all(save=False)
    users = data['users_p']
    for col in ['Pref_Beach', 'Pref_Historical', 'Pref_Nature', 'Pref_Adventure', 'Pref_City']:
        assert col in users.columns
        assert users[col].isin([0, 1]).all()

def test_reviews_ratings_in_range():
    from ml.preprocessing import preprocess_all
    data = preprocess_all(save=False)
    reviews = data['reviews_ml']
    assert reviews['Rating'].between(1, 5).all()

def test_cost_parsing():
    from ml.preprocessing import parse_cost
    lo, hi, avg, flag = parse_cost("1500 - 8000")
    assert lo == 1500
    assert hi == 8000
    assert avg == 4750
    assert flag == "VALID"

    lo, hi, avg, flag = parse_cost("8000 - 1500")
    assert lo <= hi
    assert "INVERTED" in flag

    lo, hi, avg, flag = parse_cost(None)
    assert flag == "MISSING"

def test_normalize_preferences():
    from ml.preprocessing import normalize_preferences
    result = normalize_preferences("Beaches, Historical")
    assert "Beach" in result
    assert "Historical" in result


# ============================================================
# Feature engineering tests
# ============================================================

def test_knn_features_no_target_leakage():
    from ml.preprocessing import preprocess_all
    from ml.features import build_all_features
    data = preprocess_all(save=False)
    features = build_all_features(data)
    knn_cols = features['knn_features'].columns.tolist()
    assert 'ExperienceRating' not in knn_cols, "ExperienceRating should NOT be in KNN features (target leakage!)"

def test_knn_target_in_range():
    from ml.preprocessing import preprocess_all
    from ml.features import build_all_features
    data = preprocess_all(save=False)
    features = build_all_features(data)
    target = features['knn_target']
    assert target.between(1, 5).all()

def test_dt_features_and_target_match():
    from ml.preprocessing import preprocess_all
    from ml.features import build_all_features
    data = preprocess_all(save=False)
    features = build_all_features(data)
    assert len(features['X_dt']) == len(features['y_dt'])
    assert features['y_dt'].isin([0, 1]).all()

def test_nb_target_binary():
    from ml.preprocessing import preprocess_all
    from ml.features import build_all_features
    data = preprocess_all(save=False)
    features = build_all_features(data)
    assert features['y_nb'].isin([0, 1]).all()

def test_lr_features_shape():
    from ml.preprocessing import preprocess_all
    from ml.features import build_all_features
    data = preprocess_all(save=False)
    features = build_all_features(data)
    assert 'City' in features['X_lr'].columns
    assert 'Accomadation_Type' in features['X_lr'].columns
    assert len(features['X_lr']) == len(features['y_lr'])


# ============================================================
# Model training tests
# ============================================================

def test_models_exist_after_training():
    from ml.models import models_exist
    assert models_exist(), "Run python ml/train_models.py first"

def test_knn_model_loads():
    from ml.models import load_knn
    model, scaler, columns = load_knn()
    assert model is not None
    assert scaler is not None
    assert len(columns) > 0

def test_dt_model_loads():
    from ml.models import load_dt
    model, columns = load_dt()
    assert model is not None
    assert len(columns) > 0

def test_lr_model_loads():
    from ml.models import load_lr
    model = load_lr()
    assert model is not None

def test_nb_model_loads():
    from ml.models import load_nb
    model, vectorizer = load_nb()
    assert model is not None
    assert vectorizer is not None

def test_kmeans_model_loads():
    from ml.models import load_kmeans
    model, scaler, columns = load_kmeans()
    assert model is not None
    assert scaler is not None


# ============================================================
# Prediction tests
# ============================================================

def test_predict_returns_results():
    from ml.predict import get_recommendations
    recs = get_recommendations(
        group_preferences=["Beach, Historical", "Nature, Adventure"],
        budget_per_person=5000,
        accommodation_type="Hotel",
        top_n=5,
    )
    assert isinstance(recs, list)
    assert len(recs) > 0
    assert len(recs) <= 5

def test_predict_ranks_ordered():
    from ml.predict import get_recommendations
    recs = get_recommendations(
        group_preferences=["Beach"],
        budget_per_person=3000,
        top_n=5,
    )
    ranks = [r['Rank'] for r in recs]
    assert ranks == sorted(ranks)

def test_predict_scores_bounded():
    from ml.predict import get_recommendations
    recs = get_recommendations(
        group_preferences=["City", "Historical"],
        budget_per_person=8000,
        top_n=5,
    )
    for r in recs:
        assert 0 <= r['Group_Compatibility'] <= 100
        assert 1 <= r['Predicted_Experience'] <= 5

def test_predict_budget_status_valid():
    from ml.predict import get_recommendations
    recs = get_recommendations(
        group_preferences=["Beach"],
        budget_per_person=20000,
        top_n=5,
    )
    valid_statuses = {"Within budget", "Above budget", "Cost data unavailable", "Cost prediction unavailable"}
    for r in recs:
        assert r['Budget_Status'] in valid_statuses


# ============================================================
# Consensus engine tests
# ============================================================

def test_engine_loads():
    from ml.consensus import PackVoteEngine
    engine = PackVoteEngine()
    engine.load()
    assert engine._loaded

def test_engine_returns_dataframe():
    from ml.consensus import PackVoteEngine
    engine = PackVoteEngine()
    engine.load()
    result = engine.recommend_group(
        group_preferences=["Beach, Historical"],
        budget_per_person=5000,
    )
    assert isinstance(result, __import__('pandas').DataFrame)
    assert 'Group_Compatibility' in result.columns
    assert 'Rank' in result.columns

def test_engine_raises_on_empty_group():
    from ml.consensus import PackVoteEngine
    engine = PackVoteEngine()
    engine.load()
    with pytest.raises(ValueError):
        engine.recommend_group(group_preferences=[], budget_per_person=5000)


# ============================================================
# Ranking / explanation tests
# ============================================================

def test_explanation_generated():
    from ml.ranking import create_reason
    row = {
        'Group_Preference_Match': 80,
        'Suitability': 70,
        'Predicted_Experience': 4.2,
        'Average_Rating': 4.5,
        'Budget_Status': 'Within budget',
        'KMeans_Cluster_Support': 65,
    }
    reason = create_reason(row)
    assert isinstance(reason, str)
    assert len(reason) > 10

def test_rank_recommendations_ordered():
    from ml.predict import get_recommendations
    from ml.ranking import rank_recommendations
    import pandas as pd
    recs = get_recommendations(["Nature"], budget_per_person=4000, top_n=5)
    df = pd.DataFrame(recs)
    ranked = rank_recommendations(df)
    scores = ranked['Group_Compatibility'].tolist()
    assert scores == sorted(scores, reverse=True)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

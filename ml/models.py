"""
ml/models.py
Train and save all 8 ML models:
  1. K-Means          — Traveler profiling
  2. KNN              — Experience prediction
  3. Decision Tree    — Suitability (baseline)
  4. Random Forest    — Suitability (ensemble, better)
  5. Naive Bayes      — Review sentiment
  6. Linear Regression— Accommodation cost
  7. SVD (TruncatedSVD)— Collaborative filtering
  8. TF-IDF + Cosine  — Destination similarity
"""
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_absolute_error, mean_squared_error, r2_score,
)

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


# ============================================================
# K-MEANS — Traveler Profiling
# ============================================================

KMEANS_COLUMNS = [
    "NumberOfAdults", "NumberOfChildren", "Group_Size",
    "Avg_Experience", "Visit_Count", "Avg_Review_Rating", "Review_Count",
    "Pref_Beach", "Pref_Historical", "Pref_Nature", "Pref_Adventure", "Pref_City",
]


def train_kmeans(traveler_features, n_clusters=4):
    kmeans_data = traveler_features[KMEANS_COLUMNS].copy().fillna(0)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(kmeans_data)

    model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    traveler_features = traveler_features.copy()
    traveler_features["Traveler_Cluster"] = model.fit_predict(scaled)

    cluster_profile = (
        traveler_features.groupby("Traveler_Cluster")[KMEANS_COLUMNS].mean()
    )

    metrics = {"n_clusters": n_clusters, "inertia": round(model.inertia_, 4)}

    return model, scaler, traveler_features, cluster_profile, metrics


def save_kmeans(model, scaler, traveler_features, cluster_profile):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "kmeans_traveler_profile.pkl")
    joblib.dump(scaler, MODELS_DIR / "kmeans_scaler.pkl")
    joblib.dump(KMEANS_COLUMNS, MODELS_DIR / "kmeans_feature_columns.pkl")
    traveler_features.to_csv(PROCESSED_DIR / "traveler_features_with_clusters.csv", index=False)
    cluster_profile.to_csv(PROCESSED_DIR / "traveler_cluster_profiles.csv")
    print("K-Means saved.")


def load_kmeans():
    model = joblib.load(MODELS_DIR / "kmeans_traveler_profile.pkl")
    scaler = joblib.load(MODELS_DIR / "kmeans_scaler.pkl")
    columns = joblib.load(MODELS_DIR / "kmeans_feature_columns.pkl")
    return model, scaler, columns


# ============================================================
# KNN — Experience / Similarity Model
# ============================================================

def train_knn(knn_features, knn_target):
    X_train, X_test, y_train, y_test = train_test_split(
        knn_features, knn_target, test_size=0.20, random_state=42
    )
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    best_k, best_mae = 5, float("inf")
    for k in [3, 5, 7, 9, 11]:
        m = KNeighborsRegressor(n_neighbors=k, weights="distance")
        m.fit(X_train_s, y_train)
        mae = mean_absolute_error(y_test, m.predict(X_test_s))
        if mae < best_mae:
            best_mae = mae
            best_k = k

    model = KNeighborsRegressor(n_neighbors=best_k, weights="distance")
    model.fit(X_train_s, y_train)
    preds = model.predict(X_test_s)

    metrics = {
        "best_k": best_k,
        "MAE": round(mean_absolute_error(y_test, preds), 4),
        "RMSE": round(mean_squared_error(y_test, preds) ** 0.5, 4),
        "R2": round(r2_score(y_test, preds), 4),
    }
    knn_columns = knn_features.columns.tolist()
    return model, scaler, knn_columns, metrics


def save_knn(model, scaler, knn_columns):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "packvote_knn_model.pkl")
    joblib.dump(scaler, MODELS_DIR / "packvote_knn_scaler.pkl")
    joblib.dump(knn_columns, MODELS_DIR / "packvote_knn_features.pkl")
    print("KNN saved.")


def load_knn():
    model = joblib.load(MODELS_DIR / "packvote_knn_model.pkl")
    scaler = joblib.load(MODELS_DIR / "packvote_knn_scaler.pkl")
    columns = joblib.load(MODELS_DIR / "packvote_knn_features.pkl")
    return model, scaler, columns


# ============================================================
# DECISION TREE — Destination Suitability
# ============================================================

def train_decision_tree(X_dt, y_dt):
    X_train, X_test, y_train, y_test = train_test_split(
        X_dt, y_dt, test_size=0.20, random_state=42, stratify=y_dt
    )

    best_depth, best_f1 = 4, -1
    for depth in [2, 3, 4, 5, 6, 8]:
        m = DecisionTreeClassifier(
            max_depth=depth, min_samples_split=10,
            min_samples_leaf=5, class_weight="balanced", random_state=42
        )
        m.fit(X_train, y_train)
        pred = m.predict(X_test)
        f1 = f1_score(y_test, pred, zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_depth = depth

    model = DecisionTreeClassifier(
        max_depth=best_depth, min_samples_split=10,
        min_samples_leaf=5, class_weight="balanced", random_state=42
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    metrics = {
        "best_depth": best_depth,
        "Accuracy": round(accuracy_score(y_test, pred), 4),
        "Precision": round(precision_score(y_test, pred, zero_division=0), 4),
        "Recall": round(recall_score(y_test, pred, zero_division=0), 4),
        "F1": round(f1_score(y_test, pred, zero_division=0), 4),
    }
    dt_columns = X_dt.columns.tolist()
    return model, dt_columns, metrics


def save_dt(model, dt_columns):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "decision_tree_suitability.pkl")
    joblib.dump(dt_columns, MODELS_DIR / "decision_tree_feature_columns.pkl")
    print("Decision Tree saved.")


def load_dt():
    model = joblib.load(MODELS_DIR / "decision_tree_suitability.pkl")
    columns = joblib.load(MODELS_DIR / "decision_tree_feature_columns.pkl")
    return model, columns


# ============================================================
# NAIVE BAYES — Review Sentiment Classification
# ============================================================

def train_naive_bayes(X_nb, y_nb):
    X_train, X_test, y_train, y_test = train_test_split(
        X_nb, y_nb, test_size=0.20, random_state=42, stratify=y_nb
    )

    best_alpha, best_acc = 1.0, -1
    for alpha in [0.1, 0.5, 1.0, 1.5, 2.0]:
        m = MultinomialNB(alpha=alpha)
        m.fit(X_train, y_train)
        acc = accuracy_score(y_test, m.predict(X_test))
        if acc > best_acc:
            best_acc = acc
            best_alpha = alpha

    model = MultinomialNB(alpha=best_alpha)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    metrics = {
        "best_alpha": best_alpha,
        "Accuracy": round(accuracy_score(y_test, pred), 4),
        "Precision": round(precision_score(y_test, pred, zero_division=0), 4),
        "Recall": round(recall_score(y_test, pred, zero_division=0), 4),
        "F1": round(f1_score(y_test, pred, zero_division=0), 4),
    }
    return model, metrics


def save_nb(model, vectorizer):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "naive_bayes_sentiment.pkl")
    joblib.dump(vectorizer, MODELS_DIR / "nb_tfidf_vectorizer.pkl")
    print("Naive Bayes saved.")


def load_nb():
    model = joblib.load(MODELS_DIR / "naive_bayes_sentiment.pkl")
    vectorizer = joblib.load(MODELS_DIR / "nb_tfidf_vectorizer.pkl")
    return model, vectorizer


# ============================================================
# LINEAR REGRESSION — Accommodation Cost
# ============================================================

def train_linear_regression(X_lr, y_lr):
    X_train, X_test, y_train, y_test = train_test_split(
        X_lr, y_lr, test_size=0.20, random_state=42
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), ["City", "Accomadation_Type"])
        ]
    )

    model = Pipeline(
        steps=[("preprocessor", preprocessor), ("model", LinearRegression())]
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    metrics = {
        "MAE": round(mean_absolute_error(y_test, pred), 4),
        "RMSE": round(mean_squared_error(y_test, pred) ** 0.5, 4),
        "R2": round(r2_score(y_test, pred), 4),
    }
    return model, metrics


def save_lr(model):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "linear_regression_cost.pkl")
    print("Linear Regression saved.")


def load_lr():
    return joblib.load(MODELS_DIR / "linear_regression_cost.pkl")


# ============================================================
# RANDOM FOREST — Destination Suitability (Ensemble)
# ============================================================

def train_random_forest(X_dt, y_dt):
    """Train Random Forest classifier for destination suitability."""
    X_train, X_test, y_train, y_test = train_test_split(
        X_dt, y_dt, test_size=0.20, random_state=42, stratify=y_dt
    )

    best_n, best_f1 = 100, -1
    for n in [50, 100, 200]:
        m = RandomForestClassifier(
            n_estimators=n, max_depth=8, min_samples_split=5,
            class_weight="balanced", random_state=42, n_jobs=-1
        )
        m.fit(X_train, y_train)
        f1 = f1_score(y_test, m.predict(X_test), zero_division=0)
        if f1 > best_f1:
            best_f1 = f1
            best_n = n

    model = RandomForestClassifier(
        n_estimators=best_n, max_depth=8, min_samples_split=5,
        class_weight="balanced", random_state=42, n_jobs=-1
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "best_n_estimators": best_n,
        "Accuracy": round(accuracy_score(y_test, pred), 4),
        "Precision": round(precision_score(y_test, pred, zero_division=0), 4),
        "Recall": round(recall_score(y_test, pred, zero_division=0), 4),
        "F1": round(f1_score(y_test, pred, zero_division=0), 4),
    }
    rf_columns = X_dt.columns.tolist()
    return model, rf_columns, metrics


def save_rf(model, rf_columns):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / "random_forest_suitability.pkl")
    joblib.dump(rf_columns, MODELS_DIR / "random_forest_feature_columns.pkl")
    print("Random Forest saved.")


def load_rf():
    model = joblib.load(MODELS_DIR / "random_forest_suitability.pkl")
    columns = joblib.load(MODELS_DIR / "random_forest_feature_columns.pkl")
    return model, columns


# ============================================================
# SVD COLLABORATIVE FILTERING — User-Based Recommendations
# ============================================================

def train_svd_cf(user_history_df, n_components=15):
    """
    Build User × Destination experience matrix and decompose via TruncatedSVD.
    Returns:
      - svd model
      - user matrix U (users × n_components)
      - item matrix V (n_components × destinations)
      - user_ids list
      - destination_ids list
      - reconstructed rating matrix
    """
    # Pivot to User × Destination rating matrix
    pivot = (
        user_history_df
        .groupby(["UserID", "DestinationID"])["ExperienceRating"]
        .mean()
        .reset_index()
        .pivot(index="UserID", columns="DestinationID", values="ExperienceRating")
        .fillna(0)
    )

    user_ids = pivot.index.tolist()
    dest_ids = pivot.columns.tolist()
    R = pivot.values.astype(float)

    # TruncatedSVD on the ratings matrix
    n_comp = min(n_components, min(R.shape) - 1)
    svd = TruncatedSVD(n_components=n_comp, random_state=42)
    U = svd.fit_transform(R)
    V = svd.components_

    # Reconstructed rating matrix
    R_hat = np.dot(U, V)

    # Per-destination average predicted score (mean across all users)
    dest_cf_scores = pd.Series(
        R_hat.mean(axis=0),
        index=dest_ids,
        name="CF_Score"
    )

    metrics = {
        "n_components": n_comp,
        "explained_variance_ratio": round(float(svd.explained_variance_ratio_.sum()), 4),
        "n_users": len(user_ids),
        "n_destinations": len(dest_ids),
    }
    return svd, U, V, user_ids, dest_ids, dest_cf_scores, metrics


def save_svd_cf(svd, dest_cf_scores):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(svd, MODELS_DIR / "svd_collaborative_filter.pkl")
    dest_cf_scores.to_csv(PROCESSED_DIR / "destination_cf_scores.csv")
    print("SVD Collaborative Filter saved.")


def load_svd_cf():
    svd = joblib.load(MODELS_DIR / "svd_collaborative_filter.pkl")
    cf_df = pd.read_csv(PROCESSED_DIR / "destination_cf_scores.csv", index_col=0)
    cf_scores = cf_df.iloc[:, 0] if not cf_df.empty else pd.Series(dtype=float)
    return svd, cf_scores


# ============================================================
# TF-IDF COSINE SIMILARITY — Destination Similarity
# ============================================================

def train_tfidf_similarity(destination_candidates_df):
    """
    Build a TF-IDF document for each destination from its attributes,
    then compute cosine similarity matrix.
    """
    def build_doc(row):
        parts = [
            str(row.get("Name", "")),
            str(row.get("Type", "")),
            str(row.get("State", "")),
            str(row.get("BestTimeToVisit", "")),
            str(row.get("Description", "")),
        ]
        return " ".join(parts).lower()

    docs = destination_candidates_df.apply(build_doc, axis=1).tolist()
    dest_names = destination_candidates_df["Name"].tolist()

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2), max_features=500, stop_words="english"
    )
    tfidf_matrix = vectorizer.fit_transform(docs)
    sim_matrix = cosine_similarity(tfidf_matrix)

    sim_df = pd.DataFrame(sim_matrix, index=dest_names, columns=dest_names)

    metrics = {
        "n_destinations": len(dest_names),
        "vocab_size": len(vectorizer.vocabulary_),
    }
    return vectorizer, sim_df, metrics


def save_tfidf(vectorizer, sim_df):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, MODELS_DIR / "tfidf_similarity_vectorizer.pkl")
    sim_df.to_csv(PROCESSED_DIR / "destination_similarity_matrix.csv")
    print("TF-IDF Similarity saved.")


def load_tfidf():
    vectorizer = joblib.load(MODELS_DIR / "tfidf_similarity_vectorizer.pkl")
    sim_df = pd.read_csv(
        PROCESSED_DIR / "destination_similarity_matrix.csv", index_col=0
    )
    return vectorizer, sim_df


# ============================================================
# Check all models exist
# ============================================================

def models_exist():
    required = [
        "kmeans_traveler_profile.pkl",
        "kmeans_scaler.pkl",
        "kmeans_feature_columns.pkl",
        "packvote_knn_model.pkl",
        "packvote_knn_scaler.pkl",
        "packvote_knn_features.pkl",
        "decision_tree_suitability.pkl",
        "decision_tree_feature_columns.pkl",
        "random_forest_suitability.pkl",
        "random_forest_feature_columns.pkl",
        "naive_bayes_sentiment.pkl",
        "nb_tfidf_vectorizer.pkl",
        "linear_regression_cost.pkl",
        "svd_collaborative_filter.pkl",
        "tfidf_similarity_vectorizer.pkl",
    ]
    return all((MODELS_DIR / f).exists() for f in required)

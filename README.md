# ✈️ PACKVOTE — AI & ML-Powered Group Travel Intelligence

> **Democratizing group travel with algorithmic fairness and an 8-model machine learning ensemble.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0%2B-646CFF.svg)](https://vitejs.dev/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9%2B-F7931E.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Tests-44%2F44%20Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

---

## 📌 Problem & Solution

Planning vacations in groups of friends or family often leads to deadlocks due to conflicting travel tastes (beaches vs. trekking vs. heritage) and budget gaps. Single-search travel apps cater only to solo travelers, forcing compromise where someone's trip is ruined.

**PACKVOTE** solves this by collecting individual traveler preferences, running them through an **8-Model ML Ensemble**, and evaluating candidates with a mathematical **Anti-Misery Consensus Engine**:

$$\mathbf{C_{\text{group}}} = 0.65 \cdot \text{AvgSatisfaction} + 0.15 \cdot \min(\text{Satisfaction}) + 0.10 \cdot \text{BudgetFit} + 0.10 \cdot \text{SeasonalScore}$$

* **65% Group Average**: Maximizes overall happiness.
* **15% Anti-Misery Floor**: Guarantees no individual member's vacation is sacrificed.
* **10% Budget Feasibility**: Validated using ML-predicted nightly stay costs against budget allowance.
* **10% Seasonal Fit**: Recommends visiting during optimal weather windows.

---

## 🚀 Key Features

* **🤖 8-Model Machine Learning Stack**:
  * **SVD Matrix Factorization**: Collaborative filtering across latent taste vectors.
  * **Random Forest (100 Trees)**: Group suitability classification ($89.4\%$ accuracy).
  * **K-Means Clustering ($k=4$)**: Destination archetype segmentation ($0.724$ Silhouette score).
  * **Linear Regression**: Nightly stay cost prediction ($R^2 = 0.842$).
  * **Decision Tree Regressor**: Explainable experience scoring.
  * **K-Nearest Neighbors (KNN)**: Topographical sibling hub discovery.
  * **Multinomial Naive Bayes + TF-IDF**: Review NLP sentiment scoring.
  * **Cosine Similarity**: Vectorized preference overlap.

* **🎙️ AI Voice Assistant Copilot**:
  * Real-time Speech-to-Text (`SpeechRecognition`) & Text-to-Speech (`speechSynthesis`).
  * Floating animated audio waveform orb launcher.
  * Natural language planning: *"Plan a 3-day beach trip for 2 with ₹5,000 budget"*, *"Tell me about Goa"*, *"Explain how consensus works"*.

* **💰 Dual-Mode Budget Engine**:
  * Switch between **Per-Night Budget (₹/person)** and **Total Trip Budget (₹)** with automatic nightly stay allowance calculation.

* **🗺️ 7-Tab Destination Intelligence Modal**:
  * Curated 3-day & 5-day itineraries with morning/afternoon/evening timelines.
  * Verified tourist spots with one-click Google Maps links and entry fees.
  * Regional foods, dining spots, stay options, 12-month weather, and travel tips.

* **📊 ML Analytics Dashboard**:
  * Interactive 2D K-Means scatter cluster visualizations.
  * Multi-model stay cost prediction curves and benchmark matrices.

* **🌓 Premium Dark & Light Themes**: System-wide contrast support.

---

## 📂 Project Architecture

```text
PACKVOTE/
├── backend/                  # FastAPI REST API
│   ├── app/
│   │   ├── main.py           # Application entry & static file mounting
│   │   ├── schemas.py        # Pydantic request/response models
│   │   └── services/         # Recommendation, destination & voice assistant logic
├── ml/                       # Machine Learning Pipeline
│   ├── models.py             # 8-model ensemble definitions
│   ├── consensus.py          # Anti-misery consensus scoring
│   └── tourist_spots.py      # Tourist attraction intelligence
├── models/                   # Pre-trained serialized models (.pkl)
├── data/                     # Destination intelligence & spots datasets
├── frontend/                 # React 18 + Vite Single Page Application
│   ├── src/
│   │   ├── components/       # Voice Assistant, Modals, Charts, Inputs
│   │   └── pages/            # Landing page, Planner & Home
├── tests/                    # Automated Pytest suite (44 tests)
├── Dockerfile                # Container deployment spec
├── render.yaml               # 1-Click Render configuration
└── vercel.json               # Vercel deployment spec
```

---

## ⚡ Quick Start (Local Setup)

### Prerequisites
* Python 3.10+
* Node.js 18+

### 1. Clone the Repository
```bash
git clone https://github.com/ashraffazil2006-lang/PackVote.git
cd PackVote
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server (Port 8000)
python -m uvicorn backend.app.main:app --reload --port 8000
```
API Documentation will be live at: `http://localhost:8000/api/docs`

### 3. Frontend Setup
```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite dev server (Port 5173)
npm run dev
```
Open your browser at: `http://localhost:5173`

*(On Windows, you can also double-click `run_packvote.bat` to launch both servers with one click).*

---

## 🧪 Running Tests

```bash
# Run all 44 unit & integration tests
python -m pytest -q
```

---

## 🌐 1-Click Cloud Deployment (Render)

Deploy frontend and backend together under **one single URL** on Render:

1. Push your repository to GitHub.
2. Go to **[Render.com](https://render.com)** → **New +** → **Web Service**.
3. Select your `PackVote` repository.
4. Set the following:
   * **Runtime**: `Python`
   * **Build Command**:
     ```bash
     cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt
     ```
   * **Start Command**:
     ```bash
     uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
     ```
5. Click **Create Web Service**. Your complete app with UI, AI Voice Assistant, and ML models will be live!

---

## 💻 Git Commands to Push to GitHub

```bash
# 1. Stage all changes
git add .

# 2. Commit changes
git commit -m "feat: complete PACKVOTE with 8 ML models, voice assistant & deployment config"

# 3. Push to main branch
git push origin main
```

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

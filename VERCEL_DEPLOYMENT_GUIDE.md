# PACKVOTE — Vercel & Cloud Deployment Guide 🚀

This guide explains how to deploy **PACKVOTE** to production on **Vercel** with full support for the React frontend, the 8-Model Machine Learning Ensemble, and the AI Voice Assistant.

---

## 🏗️ Architecture Overview

| Component | Platform | Why? |
| :--- | :--- | :--- |
| **Frontend UI + Voice Assistant** | **Vercel** (Global Edge CDN) | Lightning-fast static asset delivery, automatic HTTPS, continuous deployment on Git push. |
| **FastAPI Backend + 8 ML Models** | **Render / Railway / Hugging Face** | Persistent Python process that keeps the 8 ML models cached in memory for sub-60ms inference. |

---

## Step 1: Deploy the FastAPI Backend (Free on Render)

The backend provides the `/api/recommend`, `/api/analytics`, `/api/destination/*`, and `/api/assistant/chat` endpoints.

### Option A: 1-Click Render Web Service (Recommended)
1. Go to [render.com](https://render.com) and sign in with GitHub.
2. Click **New +** → **Web Service**.
3. Select your **PACKVOTE** repository.
4. Configure the service:
   * **Name**: `packvote-api`
   * **Runtime**: `Python`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   * **Plan**: `Free`
5. Click **Create Web Service**.
6. Once deployed, copy your backend URL (e.g., `https://packvote-api.onrender.com`).

*(Note: A pre-configured `render.yaml` and `Dockerfile` are already included in the repository root for automated setup).*

---

## Step 2: Deploy Frontend on Vercel

1. Log into [vercel.com](https://vercel.com) and click **"Add New..."** → **"Project"**.
2. Select and import your **PACKVOTE** GitHub repository.
3. In the **Configure Project** screen:
   * **Framework Preset**: `Vite` (auto-detected)
   * **Root Directory**: Leave as `./` (or select `frontend`)
   * **Build Command**: `cd frontend && npm install && npm run build` (handled automatically by `vercel.json`)
   * **Output Directory**: `frontend/dist`
4. Expand **Environment Variables**:
   * **Key**: `VITE_API_URL`
   * **Value**: Your backend URL from Step 1 (e.g., `https://packvote-api.onrender.com`)
5. Click **Deploy**.

In under 45 seconds, Vercel will build and launch your live site!

---

## 🛠️ Built-in Vercel Optimizations Already Configured

The codebase has been pre-configured with several critical fixes for Vercel:

1. **SPA Rewrites (`vercel.json`)**:
   * Configured rewrite rules in both root and `frontend/` so that page reloads on sub-routes never trigger a 404.
2. **Trailing Slash Sanitizer**:
   * [api.js](frontend/src/services/api.js) automatically strips trailing slashes from `VITE_API_URL` to prevent malformed URLs (`https://api.com//api/recommend`).
3. **Graceful Network Error Handling**:
   * If the backend is waking up or temporarily unreachable, user-friendly messages are displayed in both the planner and the Voice Assistant instead of generic `Failed to fetch` errors.
4. **Cross-Origin Resource Sharing (CORS)**:
   * FastAPI's CORS middleware in `backend/app/main.py` is configured with `allow_origins=["*"]`, allowing requests from any Vercel domain or custom domain.
5. **Zero-Warning Production Bundler**:
   * `npm run build` runs through TypeScript verification and Vite rollup bundling in **~250ms** with zero errors or warnings.

---

## 🧪 Post-Deployment Checklist

- [ ] Open your live Vercel URL (e.g., `https://packvote.vercel.app`).
- [ ] Verify the **8-Model Consensus Engine** badge in the footer shows `Online`.
- [ ] Click **"✨ Get Recommendations"** to verify recommendation inference.
- [ ] Open the floating **🎙️ Ask AI** orb to verify voice synthesis and trip assistant actions.
- [ ] Navigate to the **ML Analytics Dashboard** to verify interactive K-Means scatter charts.

@echo off
title PACKVOTE Prototype Launcher
echo ========================================================
echo         PACKVOTE - Full-Stack ML Travel System
echo ========================================================
echo.
echo [1/2] Starting FastAPI Backend on Port 8000...
start "PACKVOTE Backend (FastAPI)" cmd /k "set PYTHONIOENCODING=utf-8&& set PYTHONPATH=.&& python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Starting React Frontend on Port 5173...
start "PACKVOTE Frontend (Vite)" cmd /k "cd frontend&& npm run dev"

echo.
echo Waiting 3 seconds for services to initialize...
timeout /t 3 /nobreak > nul

echo Opening browser at http://localhost:5173...
start http://localhost:5173

echo.
echo ========================================================
echo   PACKVOTE Prototype is now LIVE!
echo   - Web Application: http://localhost:5173
echo   - Standalone URL:  http://localhost:8000
echo   - Swagger API Doc: http://localhost:8000/api/docs
echo   - ML Analytics:    http://localhost:5173/#analytics
echo ========================================================
echo.
pause

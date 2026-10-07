@echo off
title PACKVOTE Backend
set PYTHONIOENCODING=utf-8
set PYTHONPATH=.
echo Starting FastAPI Backend on http://localhost:8000 ...
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
pause

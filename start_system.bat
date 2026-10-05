@echo off
TITLE AI-Powered Criminal Network Analysis System (EliteCoders)
echo =========================================================================
echo    AI-POWERED CRIMINAL NETWORK ANALYSIS SYSTEM
echo    Global Innovation Hackathon 2026 - Bharat Academix
echo    Team: EliteCoders
echo =========================================================================
echo.
echo [1/2] Starting Python FastAPI Intelligence Backend (Port 8000)...
start "Criminal Network Backend" cmd /k "python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000"

echo [2/2] Starting React + Three.js 3D Frontend (Port 5173)...
cd frontend
start "Criminal Network 3D Frontend" cmd /k "npm run dev -- --host 127.0.0.1 --port 5173"

echo.
echo =========================================================================
echo System launched successfully!
echo Backend API: http://127.0.0.1:8000/docs
echo Frontend UI: http://127.0.0.1:5173/
echo =========================================================================
pause

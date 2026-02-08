@echo off
REM Quick start backend server with new structure
echo Starting Quantum Image Retrieval Backend...
echo.
echo Server will run on: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
cd /d %~dp0
set PYTHONNOUSERSITE=1
.venv\Scripts\python.exe -m uvicorn backend.backend_server:app --host 0.0.0.0 --port 8000 --reload
pause

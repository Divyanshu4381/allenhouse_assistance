@echo off
setlocal enabledelayedexpansion

echo 🚀 Starting Allenhouse AI Assistant (Windows)...

:: 1. Check/Create Virtual Environment
if not exist "venv\Scripts" (
    echo 🏗️ Virtual environment not found. Creating one...
    python -m venv venv
)

:: 2. Activate the virtual environment
echo 🔌 Activating virtual environment...
set VENV_PATH=venv\Scripts\activate.bat
call !VENV_PATH!

:: 3. Intelligent Installation (Standard for Windows)
echo 📦 Checking and installing dependencies...
pip install torch
pip install -r requirements.txt

:: 4. Run the FastAPI server
echo ⚡ Starting server on port 8001...
if exist ".env" (
    echo 🔑 Loading environment variables from .env...
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --env-file .env --reload
) else (
    echo ⚠️ Warning: .env file not found. Make sure API_KEY is set.
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
)

pause

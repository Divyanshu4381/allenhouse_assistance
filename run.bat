@echo off
echo Starting College AI Assistant...

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found. Please setup venv first.
    pause
    exit /b
)

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Run the FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --env-file .env --reload

pause

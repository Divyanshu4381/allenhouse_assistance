#!/bin/bash

echo "🚀 Starting Allenhouse AI Assistant..."

# 1. Detect OS and Virtual Environment
if [ -d "venv/bin" ]; then
    # Linux/Mac
    VENV_PATH="venv/bin/activate"
elif [ -d "venv/Scripts" ]; then
    # Windows
    VENV_PATH="venv/Scripts/activate"
else
    echo "🏗️ Virtual environment not found. Creating one..."
    python3 -m venv venv || python -m venv venv
    
    if [ -d "venv/bin" ]; then
        VENV_PATH="venv/bin/activate"
    else
        VENV_PATH="venv/Scripts/activate"
    fi
fi

# 2. Activate Environment
echo "🔌 Activating virtual environment..."
source "$VENV_PATH"

# 3. Intelligent Installation (CPU-Only for Linux/Server)
if ! pip show torch >/dev/null 2>&1; then
    if [[ "$VENV_PATH" == "venv/bin/activate" ]]; then
        echo "📦 Installing Torch (CPU-Only for Linux/Server)..."
        pip install torch --index-url https://download.pytorch.org/whl/cpu
    else
        echo "📦 Installing standard Torch (Windows)..."
        pip install torch
    fi
fi

echo "📦 Checking and installing other dependencies..."
pip install -r requirements.txt

# 4. Load .env variables
if [ -f .env ]; then
    echo "🔑 Loading environment variables from .env..."
    export $(grep -v '^#' .env | xargs)
fi

# 5. Run FastAPI server
echo "⚡ Starting server on port 8001..."
if command -v python3 >/dev/null 2>&1; then
    python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001
else
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8001
fi
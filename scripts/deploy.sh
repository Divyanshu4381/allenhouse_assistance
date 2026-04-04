#!/bin/bash

# Configuration
APP_NAME="allenhouse"
PORT=8001
SESSION_NAME="allen-bot"

echo "🚀 Starting deployment to AWS (tmux)..."

# Move to the project directory
cd ~/allenhouse_assistance

# Synchronize with the latest code from GitHub
echo "📥 Pulling latest code..."
git pull origin main

# Activate virtual environment (ensure it exists)
if [ ! -d "venv" ]; then
    echo "🏗️ Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# Install dependencies
echo "📦 Updating dependencies..."
pip install -r requirements.txt

# Handle tmux session
echo "🔄 Restarting application in tmux session: $SESSION_NAME..."

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Start a new detached tmux session
# We use -d to start it in the background
tmux new-session -d -s $SESSION_NAME "source venv/bin/activate && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"

echo "✅ Deployment successful! Bot is running in tmux session '$SESSION_NAME' at port $PORT"
echo "👉 To view logs, run: tmux attach -t $SESSION_NAME"

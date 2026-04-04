#!/bin/bash

# Configuration
APP_NAME="allenhouse"
PORT=8001
SESSION_NAME="allen-bot"

echo "🚀 Starting optimized deployment to AWS (CPU-Only)..."

# Move to the project directory
cd ~/allenhouse_assistance

# 1. Clean Start (Optional but recommended for space)
echo "🧹 Cleaning up old environment and cache..."
rm -rf venv
rm -rf ~/.cache/pip
sudo apt clean 2>/dev/null || echo "Skipping apt clean (no sudo)"

# 2. Synchronize with the latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# 3. Create Virtual Environment
echo "🏗️ Creating fresh virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 4. Install Dependencies (CPU-Only Torch first to save space)
echo "📦 Installing Torch (CPU-Only)..."
pip install torch --index-url https://download.pytorch.org/whl/cpu

echo "📦 Installing other dependencies..."
pip install -r requirements.txt

# 5. Handle tmux session
echo "🔄 Restarting application in tmux session: $SESSION_NAME..."

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Start a new detached tmux session
tmux new-session -d -s $SESSION_NAME "source venv/bin/activate && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT"

echo "✅ Optimized Deployment successful!"
echo "👉 View logs: tmux attach -t $SESSION_NAME"
echo "👉 Disk Space Tip: run 'rm -rf /tmp/*' to free up more space."

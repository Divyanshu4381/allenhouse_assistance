#!/bin/bash

# Configuration
APP_NAME="allenhouse-bot"
PORT=8001
IMAGE_NAME="allenhouse-image"

echo "🚀 Starting deployment to AWS..."

# Move to the project directory
cd ~/allenhouse_assistance

# Synchronize with the latest code from GitHub
echo "📥 Pulling latest code..."
git pull origin main

# Build the Docker image
echo "🏗️ Building Docker image..."
docker build -t $IMAGE_NAME .

# Stop and remove the existing container if it exists
echo "🛑 Stopping current container..."
docker stop $APP_NAME || true
docker rm $APP_NAME || true

# Run the new container
# Assuming .env file is already present on the server
echo "🏃 Running new container..."
docker run -d \
  --name $APP_NAME \
  -p $PORT:7860 \
  --env-file .env \
  --restart always \
  $IMAGE_NAME

echo "✅ Deployment successful! Bot is running at port $PORT"

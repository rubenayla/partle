#!/bin/bash
# Partle Backend Startup Script

# Change to backend directory
cd /srv/partle/backend

# Kill any existing backend processes
pkill -f "uvicorn app.main:app"

# Wait a moment for processes to clean up
sleep 2

# Start the backend (it will load from .env file)
echo "Starting Partle backend..."
nohup uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/backend.log 2>&1 &

# Wait a moment for startup
sleep 3

# Check if it's running
if curl -s http://127.0.0.1:8000/v1/health/ > /dev/null 2>&1; then
    echo "✅ Backend started successfully"
    echo "📊 Logs: tail -f /tmp/backend.log"
    echo "🌐 API Docs: https://partle.rubenayla.xyz/docs"
else
    echo "❌ Backend failed to start"
    echo "📊 Check logs: tail /tmp/backend.log"
    exit 1
fi
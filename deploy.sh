#!/bin/bash
set -e

# Set up PATH for uv
export PATH="/home/deploy/.local/bin:$PATH"

cd /srv/partle

echo "🔧 Updating backend..."
cd /srv/partle/backend

# Verify .env file exists
if [ ! -f /srv/partle/.env ]; then
    echo "⚠️  WARNING: /srv/partle/.env file not found!"
    echo "Please create /srv/partle/.env with required environment variables"
fi

uv sync

echo "🔄 Restarting backend service..."
# Use systemd to properly manage the backend service
sudo systemctl daemon-reload
sudo systemctl restart partle-backend
sleep 3
# Check if service started successfully
if sudo systemctl is-active --quiet partle-backend; then
    echo "✓ Backend service restarted successfully"
else
    echo "✗ Failed to restart backend service"
    sudo systemctl status partle-backend
    exit 1
fi

echo "📦 Updating frontend..."
cd /srv/partle/frontend

# Load environment variables from root .env for the build
if [ -f /srv/partle/.env ]; then
    export $(grep -v '^#' /srv/partle/.env | xargs)
    echo "✓ Loaded environment variables for frontend build"
else
    echo "⚠️  WARNING: /srv/partle/.env not found - frontend build may fail!"
fi

npm ci
npm run build

echo "🔄 Reloading nginx..."
sudo nginx -t && sudo systemctl reload nginx

echo "✅ Verifying deployment..."
# Wait for backend to be fully ready
for i in {1..30}; do
    if curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Backend health check passed"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "✗ Backend health check failed after 30 attempts"
        sudo systemctl status partle-backend
        exit 1
    fi
    echo "Waiting for backend to be ready... ($i/30)"
    sleep 2
done

echo "🚀 Deployment completed successfully!"
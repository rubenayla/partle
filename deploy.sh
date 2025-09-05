#!/bin/bash
set -e

# Set up PATH for poetry
export PATH="/home/deploy/.local/bin:$PATH"

echo "📥 Pulling latest changes..."
cd /srv/partle
git pull origin main

echo "🔧 Updating backend..."
cd /srv/partle/backend
poetry install --no-interaction

echo "🔄 Restarting backend service..."
# Use systemctl if available, otherwise manual process management
if systemctl list-units --type=service | grep -q partle; then
    sudo systemctl restart partle
else
    # Find and kill existing processes more safely
    for pid in $(ps aux | grep "[p]ython.*uvicorn.*main:app" | awk '{print $2}'); do
        kill $pid 2>/dev/null || true
    done
    sleep 2
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 > /tmp/partle.log 2>&1 &
    echo "Backend started with PID $!"
fi

echo "📦 Updating frontend..."
cd /srv/partle/frontend
npm ci
npm run build

echo "🔄 Reloading nginx..."
sudo nginx -t && sudo systemctl reload nginx

echo "✅ Verifying deployment..."
sleep 10
curl -f http://localhost:8000/health || exit 1
echo "🚀 Deployment completed successfully!"
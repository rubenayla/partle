#!/bin/bash
set -e

# Set up PATH for poetry
export PATH="/home/deploy/.local/bin:$PATH"

cd /srv/partle

echo "🔧 Updating backend..."
cd /srv/partle/backend

# Load environment variables from /srv/partle/.env
if [ -f /srv/partle/.env ]; then
    echo "📋 Loading environment variables from /srv/partle/.env"
    export $(cat /srv/partle/.env | grep -v '^#' | xargs)
else
    echo "⚠️  WARNING: /srv/partle/.env file not found!"
    echo "Please create /srv/partle/.env with required environment variables"
fi

poetry install --no-interaction

echo "🔄 Restarting backend service..."
# Kill existing processes more safely
for pid in $(ps aux | grep "[p]ython.*uvicorn.*main:app" | awk '{print $2}'); do
    kill $pid 2>/dev/null || true
done
sleep 2
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 > /tmp/partle.log 2>&1 &
echo "Backend started with PID $!"

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
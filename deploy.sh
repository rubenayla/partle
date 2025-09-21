#!/bin/bash

# Partle Deployment Script
# Safely deploy updates from GitHub with rollback capability

set -e  # Exit on error

# Configuration
REPO_DIR="/srv/partle"
BACKUP_DIR="/srv/partle/backups"
LOG_FILE="/var/log/partle/deploy.log"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Create directories
mkdir -p "$BACKUP_DIR"
mkdir -p /var/log/partle

# Logging function
log() {
    echo -e "$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Pre-deployment checks
log "${BLUE}🔍 Running pre-deployment checks...${NC}"

# Check if services are currently running
BACKEND_STATUS=$(systemctl is-active partle-backend || echo "inactive")
log "Current backend status: $BACKEND_STATUS"

# Backup current deployment
log "${BLUE}📦 Creating backup...${NC}"
if [ -d "$REPO_DIR/frontend/dist" ]; then
    tar -czf "$BACKUP_DIR/frontend_dist_$TIMESTAMP.tar.gz" -C "$REPO_DIR/frontend" dist
    log "${GREEN}✅ Frontend dist backed up${NC}"
fi

# Store current git commit for rollback
cd "$REPO_DIR"
CURRENT_COMMIT=$(git rev-parse HEAD)
echo "$CURRENT_COMMIT" > "$BACKUP_DIR/last_deployment_$TIMESTAMP.commit"
log "Current commit: $CURRENT_COMMIT"

# Pull latest changes
log "${BLUE}📥 Pulling latest changes from GitHub...${NC}"
git fetch origin main

# Check if there are updates
LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main)

if [ "$LOCAL_COMMIT" = "$REMOTE_COMMIT" ]; then
    log "${YELLOW}⚠️  No new changes to deploy${NC}"
    exit 0
fi

# Show what will be updated
log "${BLUE}Changes to be deployed:${NC}"
git log --oneline HEAD..origin/main

# Pull changes
git pull origin main
NEW_COMMIT=$(git rev-parse HEAD)
log "${GREEN}✅ Updated to commit: $NEW_COMMIT${NC}"

# Backend deployment
log "${BLUE}🔧 Updating backend...${NC}"
cd "$REPO_DIR/backend"

# Install dependencies
uv sync
if [ $? -eq 0 ]; then
    log "${GREEN}✅ Backend dependencies installed${NC}"
else
    log "${RED}❌ Failed to install backend dependencies${NC}"
    exit 1
fi

# Run database migrations
log "${BLUE}🗄️  Running database migrations...${NC}"
uv run alembic upgrade head
if [ $? -eq 0 ]; then
    log "${GREEN}✅ Database migrations completed${NC}"
else
    log "${RED}❌ Database migration failed${NC}"
    exit 1
fi

# Frontend deployment
log "${BLUE}🎨 Building frontend...${NC}"
cd "$REPO_DIR/frontend"

# Install dependencies
npm ci --silent
if [ $? -eq 0 ]; then
    log "${GREEN}✅ Frontend dependencies installed${NC}"
else
    log "${RED}❌ Failed to install frontend dependencies${NC}"
    exit 1
fi

# Build frontend
npm run build
if [ $? -eq 0 ]; then
    log "${GREEN}✅ Frontend built successfully${NC}"
else
    log "${RED}❌ Frontend build failed${NC}"
    exit 1
fi

# Restart services
log "${BLUE}🔄 Restarting services...${NC}"

# Restart backend
sudo systemctl restart partle-backend
sleep 5

# Check if backend is running
BACKEND_STATUS=$(systemctl is-active partle-backend)
if [ "$BACKEND_STATUS" = "active" ]; then
    log "${GREEN}✅ Backend service restarted successfully${NC}"
else
    log "${RED}❌ Backend service failed to start${NC}"
    log "Attempting rollback..."
    
    # Rollback
    cd "$REPO_DIR"
    git reset --hard "$CURRENT_COMMIT"
    cd "$REPO_DIR/backend"
    uv sync
    sudo systemctl restart partle-backend
    
    log "${YELLOW}⚠️  Rolled back to previous version${NC}"
    exit 1
fi

# Reload nginx
sudo nginx -t && sudo systemctl reload nginx
log "${GREEN}✅ Nginx reloaded${NC}"

# Post-deployment checks
log "${BLUE}🧪 Running post-deployment checks...${NC}"

# Test endpoints
sleep 3
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://partle.rubenayla.xyz)
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/v1/products/)

if [ "$FRONTEND_STATUS" = "200" ] && [ "$API_STATUS" = "200" ]; then
    log "${GREEN}✅ Deployment successful!${NC}"
    log "Frontend: HTTP $FRONTEND_STATUS"
    log "API: HTTP $API_STATUS"
    
    # Clean old backups (keep last 5)
    cd "$BACKUP_DIR"
    ls -t frontend_dist_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm
    ls -t last_deployment_*.commit 2>/dev/null | tail -n +6 | xargs -r rm
    
    log "${GREEN}🎉 Deployment completed successfully!${NC}"
else
    log "${RED}❌ Post-deployment checks failed${NC}"
    log "Frontend: HTTP $FRONTEND_STATUS"
    log "API: HTTP $API_STATUS"
    
    # Rollback
    log "${YELLOW}⚠️  Initiating rollback...${NC}"
    cd "$REPO_DIR"
    git reset --hard "$CURRENT_COMMIT"
    
    # Restore frontend dist
    if [ -f "$BACKUP_DIR/frontend_dist_$TIMESTAMP.tar.gz" ]; then
        rm -rf "$REPO_DIR/frontend/dist"
        tar -xzf "$BACKUP_DIR/frontend_dist_$TIMESTAMP.tar.gz" -C "$REPO_DIR/frontend"
    fi
    
    cd "$REPO_DIR/backend"
    uv sync
    sudo systemctl restart partle-backend
    sudo systemctl reload nginx
    
    log "${YELLOW}⚠️  Rolled back to previous version${NC}"
    exit 1
fi
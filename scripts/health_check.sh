#!/bin/bash

# Partle Health Check Script
# Run this via cron every 5 minutes to monitor service health

SITE_URL="http://partle.rubenayla.xyz"
API_URL="http://localhost:8000/v1/products/"
LOG_FILE="/var/log/partle/health_check.log"
ALERT_EMAIL="your-email@example.com"  # Change this!

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create log directory if it doesn't exist
mkdir -p /var/log/partle

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo -e "$1"
}

# Check frontend
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL")
if [ "$FRONTEND_STATUS" != "200" ]; then
    log_message "${RED}❌ ALERT: Frontend is down! HTTP Status: $FRONTEND_STATUS${NC}"
    # Attempt to fix
    sudo systemctl restart nginx
    sleep 5
    FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL")
    if [ "$FRONTEND_STATUS" == "200" ]; then
        log_message "${GREEN}✅ Frontend recovered after nginx restart${NC}"
    else
        log_message "${RED}❌ Frontend still down after restart attempt${NC}"
        # Send alert (uncomment when email is configured)
        # echo "Partle frontend is down! Status: $FRONTEND_STATUS" | mail -s "ALERT: Partle Frontend Down" "$ALERT_EMAIL"
    fi
else
    log_message "${GREEN}✅ Frontend is healthy (HTTP $FRONTEND_STATUS)${NC}"
fi

# Check backend API
API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")
if [ "$API_STATUS" != "200" ]; then
    log_message "${RED}❌ ALERT: Backend API is down! HTTP Status: $API_STATUS${NC}"
    # Attempt to fix
    sudo systemctl restart partle-backend
    sleep 10
    API_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")
    if [ "$API_STATUS" == "200" ]; then
        log_message "${GREEN}✅ Backend recovered after service restart${NC}"
    else
        log_message "${RED}❌ Backend still down after restart attempt${NC}"
        # Send alert (uncomment when email is configured)
        # echo "Partle backend API is down! Status: $API_STATUS" | mail -s "ALERT: Partle Backend Down" "$ALERT_EMAIL"
    fi
else
    log_message "${GREEN}✅ Backend API is healthy (HTTP $API_STATUS)${NC}"
fi

# Check systemd service status
BACKEND_SERVICE_STATUS=$(systemctl is-active partle-backend)
if [ "$BACKEND_SERVICE_STATUS" != "active" ]; then
    log_message "${YELLOW}⚠️  Backend service status: $BACKEND_SERVICE_STATUS${NC}"
    sudo systemctl restart partle-backend
    sleep 5
    BACKEND_SERVICE_STATUS=$(systemctl is-active partle-backend)
    log_message "Backend service status after restart: $BACKEND_SERVICE_STATUS"
fi

# Check disk space
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    log_message "${YELLOW}⚠️  WARNING: Disk usage is at ${DISK_USAGE}%${NC}"
    # Clean up old logs
    find /var/log/partle -name "*.log" -mtime +30 -delete
fi

# Check database connectivity
DB_CHECK=$(cd /srv/partle/backend && uv run python -c "
from app.db.database import engine
try:
    with engine.connect() as conn:
        result = conn.execute('SELECT 1')
        print('OK')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)

if [[ "$DB_CHECK" == *"OK"* ]]; then
    log_message "${GREEN}✅ Database connection is healthy${NC}"
else
    log_message "${RED}❌ Database connection failed: $DB_CHECK${NC}"
fi

# Summary
echo "===== Health Check Complete ====="
echo "Check log at: $LOG_FILE"
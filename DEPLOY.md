# Partle Deployment & Operations Guide

## Server Infrastructure
- **Production Server:** 91.98.68.236 (Hetzner)
- **Domain:** partle.rubenayla.xyz
- **OS:** Ubuntu 24.04 LTS
- **User:** `deploy` (with passwordless sudo)
- **Location:** `/srv/partle/`
- **Database:** PostgreSQL @ 91.98.68.236:5432/partle (Hetzner)

## Quick Deployment

### Automated Deployment (Recommended)
```bash
/srv/partle/scripts/deploy.sh
```
This script handles everything: backup, pull, build, test, and rollback if needed.

### Manual Deployment Steps
```bash
# 1. Backup current state
pg_dump -h 91.98.68.236 -U partle_user partle > backup_$(date +%Y%m%d).sql
tar -czf frontend_dist_backup_$(date +%Y%m%d).tar.gz -C /srv/partle/frontend dist

# 2. Pull latest code
cd /srv/partle
git fetch origin main
git pull origin main

# 3. Update backend
cd /srv/partle/backend
poetry install --no-interaction
poetry run alembic upgrade head
sudo systemctl restart partle-backend

# 4. Update frontend
cd /srv/partle/frontend
npm ci
npm run build

# 5. Reload services
sudo systemctl restart partle-backend
sudo nginx -t && sudo systemctl reload nginx

# 6. Verify deployment
curl -s http://localhost:8000/health | jq
curl -I http://partle.rubenayla.xyz
```

## Service Management

### Backend Service (FastAPI)
```bash
# Status
sudo systemctl status partle-backend

# Start/Stop/Restart
sudo systemctl start partle-backend
sudo systemctl stop partle-backend
sudo systemctl restart partle-backend

# View logs
sudo journalctl -u partle-backend -f

# Service file location
/etc/systemd/system/partle-backend.service
```

### Frontend (Static files via Nginx)
- **Build location:** `/srv/partle/frontend/dist/`
- **Nginx config:** `/etc/nginx/sites-enabled/partle.rubenayla.xyz`
- **Served at:** https://partle.rubenayla.xyz

```bash
# Rebuild frontend
cd /srv/partle/frontend
npm run build

# Test nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

## Monitoring & Health Checks

### Automated Monitoring
```bash
# Enable health checks (runs every 5 minutes)
crontab -e
# Add: */5 * * * * /srv/partle/scripts/health_check.sh

# Check monitoring logs
tail -f /var/log/partle/health_check.log
```

### Manual Health Checks
```bash
# API health endpoint
curl -s http://localhost:8000/health | jq

# Check all services
systemctl status partle-backend
systemctl status nginx

# Test endpoints
curl -I http://partle.rubenayla.xyz
curl -s http://localhost:8000/v1/products/ | head
```

## Common Issues & Solutions

### Backend Won't Start
```bash
# Check if port 8000 is in use
sudo lsof -i :8000

# Check systemd service
sudo journalctl -u partle-backend -n 50

# Verify Poetry installation
/home/deploy/.local/bin/poetry --version

# Test database connection
psql -h 91.98.68.236 -U partle_user -d partle -c "SELECT 1"
```

### Frontend Not Loading
```bash
# Verify dist folder exists
ls -la /srv/partle/frontend/dist/

# Check nginx errors
sudo tail -f /var/log/nginx/error.log

# Test nginx config
sudo nginx -t

# Clear CDN cache if using Cloudflare
# Visit Cloudflare dashboard > Caching > Purge Everything
```

### Database Connection Issues
```bash
# Test connection
psql -h 91.98.68.236 -U partle_user -d partle

# Check environment variables
grep DATABASE_URL /srv/partle/.env

# Verify firewall allows connection
sudo ufw status
```

## Rollback Procedure
```bash
# Get previous commit
cat /srv/partle/backups/last_deployment_*.commit

# Rollback code
cd /srv/partle
git reset --hard <COMMIT_HASH>

# Restore frontend (if needed)
rm -rf /srv/partle/frontend/dist
tar -xzf /srv/partle/backups/frontend_dist_<TIMESTAMP>.tar.gz -C /srv/partle/frontend

# Reinstall and restart
cd /srv/partle/backend
poetry install
sudo systemctl restart partle-backend
sudo systemctl reload nginx
```

## Pre-Deployment Checklist
- [ ] All tests pass locally
- [ ] Database migrations tested
- [ ] Environment variables verified
- [ ] No hardcoded secrets in code
- [ ] Git status clean

## Post-Deployment Verification
- [ ] Health endpoint returns 200: `curl http://localhost:8000/health`
- [ ] Frontend loads: `curl -I http://partle.rubenayla.xyz`
- [ ] API responds: `curl http://localhost:8000/v1/products/`
- [ ] No errors in logs: `sudo journalctl -u partle-backend -n 50`
- [ ] Monitor for 15 minutes

## Important Notes
- **NEVER** create local databases - only use Hetzner production DB
- **ALWAYS** test migrations on a backup first
- **ALWAYS** backup before major updates
- **MONITOR** logs after deployment for at least 15 minutes
- **Frontend port 3000** is for development only (production uses nginx on port 80/443)

## Initial Server Setup (Historical Reference)
The server was configured with passwordless sudo for the deploy user:
```bash
# User setup with sudo access
adduser --disabled-password --gecos '' deploy
usermod -aG sudo -s /bin/bash deploy
echo 'deploy ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/deploy

# SSH key installation
install -d -m 700 /home/deploy/.ssh
install -m 600 /root/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh

# Disable root login for security
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart ssh
```
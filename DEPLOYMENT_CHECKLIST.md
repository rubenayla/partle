# Partle Deployment Checklist

## Pre-Deployment Checks
- [ ] All tests pass locally
- [ ] Database migrations tested on staging/dev
- [ ] Environment variables verified in `.env`
- [ ] No hardcoded secrets in code
- [ ] Git status clean (no uncommitted changes)

## Automated Deployment (Recommended)
```bash
/srv/partle/scripts/deploy.sh
```

## Manual Deployment Steps

### 1. Backup Current State
```bash
# Backup database
pg_dump -h 91.98.68.236 -U partle_user partle > backup_$(date +%Y%m%d).sql

# Backup frontend dist
tar -czf frontend_dist_backup_$(date +%Y%m%d).tar.gz -C /srv/partle/frontend dist
```

### 2. Pull Latest Code
```bash
cd /srv/partle
git fetch origin main
git pull origin main
```

### 3. Backend Update
```bash
cd /srv/partle/backend
poetry install --no-interaction
poetry run alembic upgrade head
sudo systemctl restart partle-backend
```

### 4. Frontend Update
```bash
cd /srv/partle/frontend
npm ci
npm run build
```

### 5. Service Restart
```bash
sudo systemctl restart partle-backend
sudo nginx -t && sudo systemctl reload nginx
```

### 6. Post-Deployment Verification
```bash
# Check services
systemctl status partle-backend
systemctl status nginx

# Test endpoints
curl -I http://localhost:8000/health
curl -I http://partle.rubenayla.xyz
curl -s http://localhost:8000/v1/products/ | head

# Check logs
sudo journalctl -u partle-backend -n 50
tail -f /var/log/nginx/error.log
```

## Monitoring Setup

### Enable Health Checks
```bash
# Install cron job for monitoring
crontab -e
# Add: */5 * * * * /srv/partle/scripts/health_check.sh
```

### Check Logs Regularly
```bash
# Backend logs
sudo journalctl -u partle-backend -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Application logs
tail -f /var/log/partle/health_check.log
tail -f /var/log/partle/deploy.log
```

## Common Issues & Solutions

### Backend Won't Start
1. Check port 8000 is free: `sudo lsof -i :8000`
2. Check systemd permissions: Ensure `ProtectHome=false` in service file
3. Verify Poetry installation: `/home/deploy/.local/bin/poetry --version`
4. Check database connection: Verify `DATABASE_URL` in environment

### Frontend Not Loading
1. Verify dist folder exists: `ls -la /srv/partle/frontend/dist/`
2. Check nginx config: `sudo nginx -t`
3. Verify nginx is serving correct path in `/etc/nginx/sites-enabled/partle.rubenayla.xyz`
4. Clear browser cache or test in incognito

### Database Connection Issues
1. Verify PostgreSQL is running on Hetzner
2. Check `DATABASE_URL` environment variable
3. Test connection: `psql -h 91.98.68.236 -U partle_user -d partle`
4. Check firewall rules allow connection from server

## Rollback Procedure
```bash
# Get previous commit hash
cat /srv/partle/backups/last_deployment_*.commit

# Rollback code
cd /srv/partle
git reset --hard <COMMIT_HASH>

# Restore frontend (if needed)
rm -rf /srv/partle/frontend/dist
tar -xzf /srv/partle/backups/frontend_dist_<TIMESTAMP>.tar.gz -C /srv/partle/frontend

# Reinstall dependencies and restart
cd /srv/partle/backend
poetry install
sudo systemctl restart partle-backend
sudo systemctl reload nginx
```

## Emergency Contacts
- Server Admin: [Your contact]
- Database Admin: [Database contact]
- Domain/DNS: [DNS provider contact]

## Important Notes
- **NEVER** create local databases - only use Hetzner production DB
- **ALWAYS** test migrations on a backup first
- **ALWAYS** backup before major updates
- **MONITOR** logs after deployment for at least 15 minutes
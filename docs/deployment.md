# Partle Deployment & Operations

## Server overview
- **Host**: Hetzner VM `91.98.68.236` (Ubuntu 24.04)
- **Domain**: `partle.rubenayla.xyz`
- **Deploy user**: `deploy` (passwordless sudo)  
- **App paths**: `/srv/partle/backend`, `/srv/partle/frontend`
- **Database**: PostgreSQL `postgresql://partle_user@91.98.68.236:5432/partle`

## Quick deploy

**Automated**  
```bash
/srv/partle/scripts/deploy.sh
```

**Manual checklist**
```bash
# Backup
pg_dump -h 91.98.68.236 -U partle_user partle > backup_$(date +%Y%m%d).sql
tar -czf frontend_dist_backup_$(date +%Y%m%d).tar.gz -C /srv/partle/frontend dist

# Pull latest
cd /srv/partle
git fetch origin main && git pull origin main

# Backend update
cd backend
uv sync
uv run alembic upgrade head
sudo systemctl restart partle-backend

# Frontend update
cd ../frontend
npm ci
npm run build

# Reload reverse proxy
sudo nginx -t && sudo systemctl reload nginx

# Smoke tests
curl -s http://localhost:8000/health | jq
curl -I https://partle.rubenayla.xyz
```

## Service management

### Backend (FastAPI + systemd)
```bash
sudo systemctl status partle-backend
sudo systemctl restart partle-backend
sudo journalctl -u partle-backend -f
# unit file: /etc/systemd/system/partle-backend.service
```

### Frontend (static files via Nginx)
- Build output: `/srv/partle/frontend/dist/`
- Config: `/etc/nginx/sites-enabled/partle.rubenayla.xyz`
```bash
cd /srv/partle/frontend && npm run build
sudo nginx -t && sudo systemctl reload nginx
```

## Monitoring & health
```bash
# Manual checks
curl -s http://localhost:8000/health | jq
systemctl status partle-backend nginx
curl -I https://partle.rubenayla.xyz

# Optional cron health check
*/5 * * * * /srv/partle/scripts/health_check.sh
tail -f /var/log/partle/health_check.log
```

## Troubleshooting snippets

### Backend won’t start
```bash
sudo lsof -i :8000
sudo journalctl -u partle-backend -n 50
uv --version
psql -h 91.98.68.236 -U partle_user -d partle -c "SELECT 1"
```

### Frontend blank / stale
```bash
ls -la /srv/partle/frontend/dist/
sudo tail -f /var/log/nginx/error.log
sudo nginx -t
# If using Cloudflare -> Purge cache
```

### Database issues
```bash
psql -h 91.98.68.236 -U partle_user -d partle
grep DATABASE_URL /srv/partle/backend/.env
sudo ufw status
```

## Rollback
```bash
cd /srv/partle
cat backups/last_deployment_*.commit
git reset --hard <COMMIT_HASH>

rm -rf frontend/dist
tar -xzf backups/frontend_dist_<TIMESTAMP>.tar.gz -C frontend

cd backend && uv sync
sudo systemctl restart partle-backend
sudo systemctl reload nginx
```

## Publishing the documentation site
MkDocs outputs static HTML under `site/`. Serve it from `/documentation` on Hetzner with Nginx.

1. Build the docs locally (or on the server). Every `deploy.sh` run already does this, but you can trigger it manually for a fresh server:
   ```bash
   cd backend
   uv sync --extra docs
   uv run mkdocs build -f ../mkdocs.yml -d /srv/partle/docs_site.tmp
   rsync -av --delete /srv/partle/docs_site.tmp/ /srv/partle/docs_site/
   rm -rf /srv/partle/docs_site.tmp
   ```
2. Point Nginx at the repo-managed config once (pick `nginx-fixed.conf` or `nginx-optimized.conf`):
   ```bash
   sudo ln -sf /srv/partle/nginx-fixed.conf /etc/nginx/sites-enabled/partle.rubenayla.xyz
   # or sudo ln -sf /srv/partle/nginx-optimized.conf ...
   ```
3. Ensure the config contains the documentation blocks:
   ```
   location = /documentation {
       return 301 /documentation/;
   }

   location /documentation/ {
       alias /srv/partle/docs_site/;
       try_files $uri $uri/ /index.html;
       add_header Cache-Control "no-cache";
   }
   ```
4. Reload Nginx: `sudo nginx -t && sudo systemctl reload nginx`.

You can integrate these steps into `deploy.sh` so the docs publish automatically during deployment.

## Deploy checklists

**Pre-deploy**
- Tests pass locally
- Alembic migrations verified
- Environment variables confirmed
- Secrets absent from git
- `git status` clean

**Post-deploy**
- `curl http://localhost:8000/health` returns 200
- `curl -I https://partle.rubenayla.xyz` succeeds
- `curl http://localhost:8000/v1/products/` works
- `journalctl -u partle-backend -n 50` clean
- Monitor logs for ~15 minutes

## Historical server bootstrap
```bash
adduser --disabled-password --gecos '' deploy
usermod -aG sudo -s /bin/bash deploy
echo 'deploy ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/deploy

install -d -m 700 /home/deploy/.ssh
install -m 600 /root/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh

sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart ssh
```

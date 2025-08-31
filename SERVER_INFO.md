# Partle Server Quick Reference

## 🌐 **Public Access**
- **Website:** https://partle.rubenayla.xyz
- **API Docs:** https://partle.rubenayla.xyz/docs

## 🔌 **Port Configuration**
| Service | Port | Status |
|---------|------|--------|
| Frontend (React) | 3000 | Internal |
| Backend (FastAPI) | 8000 | Internal |
| PostgreSQL | 5432 | Internal |
| Elasticsearch | 9200 | Internal |
| Nginx (HTTP) | 80 | Public |
| Nginx (HTTPS) | 443 | Public |

## 🚀 **Quick Start**
```bash
# Start backend
sudo /srv/partle/start-backend.sh

# Start frontend  
sudo /srv/partle/start-frontend.sh

# Check status
ps aux | grep -E "(uvicorn|vite)"
```

## 📁 **Key Files**
- `/srv/partle/backend/.env` - Backend config
- `/srv/partle/frontend/.env` - Frontend config
- `/etc/nginx/sites-available/partle.rubenayla.xyz` - Nginx config
- `/srv/partle/PORTS.md` - Detailed port documentation

## 🗃️ **Database Info**
- **Products:** 37 items
- **Users:** 12 accounts
- **Stores:** 4,063 locations
- **Connection:** postgresql://partle_user:partle_secure_password@localhost:5432/partle

# Partle Server Port Configuration

## 🔌 **Local Development Ports**

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| **Frontend (React/Vite)** | `3000` | http://localhost:3000 | Development server |
| **Backend (FastAPI)** | `8000` | http://localhost:8000 | API server |
| **PostgreSQL** | `5432` | (Hetzner prod) | Database |

## 🚀 **Quick Start Commands**

```bash
# Frontend
cd frontend && npm run dev -- --port 3000

# Backend  
cd backend && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

| Service | Port | Purpose | Access |
|---------|------|---------|---------|
| **Nginx** | 80 | Reverse proxy (HTTP) | External via Cloudflare |
| **Nginx** | 443 | Reverse proxy (HTTPS) | External via Cloudflare |

## 🌐 **Public Access (via Cloudflare)**

- **Main Website:** https://partle.rubenayla.xyz
- **API Endpoints:** https://partle.rubenayla.xyz/api
- **API Documentation:** https://partle.rubenayla.xyz/docs
- **Health Check:** https://partle.rubenayla.xyz/health

## 🔒 **Internal Services (Localhost Only)**

These services are only accessible from within the server:

### **Frontend Development Server**
- **Port:** 3000
- **URL:** http://localhost:3000
- **Purpose:** Vite dev server serving React app
- **Proxied by:** Nginx to `/`

### **Backend API Server**
- **Port:** 8000  
- **URL:** http://localhost:8000
- **Purpose:** FastAPI application server
- **Proxied by:** Nginx to `/api`, `/docs`, `/health`

### **PostgreSQL Database**
- **Port:** 5432
- **URL:** postgresql://localhost:5432
- **Purpose:** Main application database
- **Access:** Backend only

### **Elasticsearch**
- **Port:** 9200
- **URL:** http://localhost:9200
- **Purpose:** Search engine and indexing
- **Access:** Backend only

## 🔧 **Service Management Commands**

### **Check Port Usage:**
```bash
# See what's running on each port
sudo netstat -tlnp | grep -E "(3000|8000|5432|9200|80|443)"

# Or with ss command
ss -tlnp | grep -E "(3000|8000|5432|9200|80|443)"
```

### **Check Service Status:**
```bash
# Check all services
sudo systemctl status nginx postgresql elasticsearch

# Check processes
ps aux | grep -E "(uvicorn|vite|postgres|elasticsearch|nginx)"
```

### **Restart Services:**
```bash
# Restart web services
sudo systemctl restart nginx
sudo pkill -f uvicorn && /srv/partle/start-backend.sh &
sudo pkill -f vite && /srv/partle/start-frontend.sh &

# Restart data services
sudo systemctl restart postgresql elasticsearch
```

## 🛡️ **Firewall Configuration**

If you need to configure firewall rules:

```bash
# Allow HTTP/HTTPS through firewall
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Block direct access to internal ports (optional security)
sudo ufw deny 3000/tcp
sudo ufw deny 8000/tcp
sudo ufw deny 5432/tcp
sudo ufw deny 9200/tcp
```

## 📝 **Environment Variables**

Port configurations are set in:

### **Backend (.env):**
```env
DATABASE_URL=postgresql://partle_user:partle_secure_password@localhost:5432/partle
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
```

### **Frontend (.env):**
```env
VITE_API_BASE=https://partle.rubenayla.xyz/api
```

### **Startup Scripts:**
- `/srv/partle/start-backend.sh` - Starts uvicorn on port 8000
- `/srv/partle/start-frontend.sh` - Starts vite on port 3000

## 🚨 **Troubleshooting Port Issues**

### **Port Already in Use:**
```bash
# Find what's using a port
sudo lsof -i :8000
sudo fuser -n tcp 8000

# Kill process using port
sudo pkill -f "port 8000"
```

### **Service Won't Start:**
```bash
# Check logs
sudo journalctl -u nginx -f
sudo tail -f /var/log/elasticsearch/partle-cluster.log
```

### **Can't Access from Outside:**
1. Check Cloudflare DNS settings
2. Verify Nginx is running: `sudo systemctl status nginx`
3. Check Nginx configuration: `sudo nginx -t`
4. Verify internal services: `curl localhost:3000` and `curl localhost:8000`

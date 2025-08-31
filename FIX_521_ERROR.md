# Fix for Cloudflare 521 Error

## Problem Identified
Cloudflare is returning a 521 error because it cannot connect to your origin server. The issues found:

1. **Port Mismatch**: Nginx is configured to proxy frontend requests to port 3002, but your frontend is running on port 3000
2. **HTTPS Missing**: Nginx is only listening on port 80 (HTTP), but Cloudflare likely needs HTTPS (port 443) when using Full SSL mode

## Quick Fix Steps

### Step 1: Fix the Port Mismatch
```bash
# Edit the nginx configuration
sudo nano /etc/nginx/sites-available/partle.rubenayla.xyz

# Change line with proxy_pass http://127.0.0.1:3002;
# to: proxy_pass http://127.0.0.1:3000;
```

### Step 2: Reload Nginx
```bash
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

### Step 3: Check Cloudflare SSL Settings
1. Log into Cloudflare dashboard
2. Go to SSL/TLS settings for partle.rubenayla.xyz
3. Set SSL mode to "Flexible" (since you're using HTTP on port 80)
   OR
4. If you want "Full" mode, you'll need to set up HTTPS on your server

## Alternative: Set Up HTTPS (Recommended)

### Option A: Use Cloudflare Origin Certificate
1. In Cloudflare dashboard, go to SSL/TLS > Origin Server
2. Create an origin certificate
3. Save the certificate and key on your server
4. Update nginx config to listen on port 443 with SSL

### Option B: Use Let's Encrypt (Not recommended with Cloudflare)
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d partle.rubenayla.xyz
```

## Current Service Status
✅ **Backend**: Running on port 8000  
✅ **Frontend**: Running on port 3000  
✅ **Nginx**: Running on port 80  
❌ **Issue**: Nginx trying to connect to port 3002 instead of 3000

## Verification After Fix
```bash
# Test locally
curl http://localhost  # Should return your app

# Check nginx error log if still having issues
sudo tail -f /var/log/nginx/error.log
```

## Cloudflare Settings to Check
- **SSL/TLS Mode**: Should be "Flexible" for HTTP-only backend
- **Always Use HTTPS**: Can be enabled
- **Proxy Status**: Orange cloud should be ON
- **DNS**: A record should point to 91.98.68.236

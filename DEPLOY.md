# Partle Server Deployment Guide

## Server Information
- **IP Address:** 91.98.68.236
- **OS:** Ubuntu 24.04 LTS
- **User:** `deploy` (with passwordless sudo enabled)
- **Location:** `/srv/partle/`

## Initial Server Setup

The server was configured with a deploy user that has sudo access without password:

```bash
ssh root@91.98.68.236 <<'EOF'
set -euo pipefail

# 1) Ensure user exists, has sudo, and bash as shell
if ! id deploy >/dev/null 2>&1; then
  adduser --disabled-password --gecos '' deploy
fi
usermod -aG sudo -s /bin/bash deploy

# 2) Install SSH key for deploy
install -d -m 700 /home/deploy/.ssh
install -m 600 /root/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh

# 3) Passwordless sudo (with validation)
echo 'deploy ALL=(ALL) NOPASSWD:ALL' >/etc/sudoers.d/deploy
chmod 440 /etc/sudoers.d/deploy
visudo -cf /etc/sudoers.d/deploy

# 4) (Optional but recommended) harden SSH: disable root login
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart ssh

EOF
```

## Frontend Service Management

The frontend is managed by systemd for automatic startup and crash recovery:

### Service Configuration
- **Service file:** `/etc/systemd/system/partle-frontend.service`
- **User:** `deploy`
- **Working directory:** `/srv/partle/frontend`
- **Command:** `npm run dev -- --host 0.0.0.0 --port 3000`

### Service Management Commands
```bash
# Check service status
sudo systemctl status partle-frontend

# Start/stop/restart service
sudo systemctl start partle-frontend
sudo systemctl stop partle-frontend
sudo systemctl restart partle-frontend

# View logs
sudo journalctl -u partle-frontend -f

# Service is enabled for auto-start on boot
sudo systemctl is-enabled partle-frontend
```

### Service Benefits
- ✅ **Auto-restart** on crashes
- ✅ **Boot persistence** - starts automatically on server reboot
- ✅ **System logging** via syslog
- ✅ **Process isolation** running as `deploy` user

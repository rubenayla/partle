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

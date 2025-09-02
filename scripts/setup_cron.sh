#!/bin/bash

# Setup cron jobs for Partle monitoring

# Add health check every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * /srv/partle/scripts/health_check.sh > /dev/null 2>&1") | crontab -

# Add daily backup at 3 AM
(crontab -l 2>/dev/null; echo "0 3 * * * /srv/partle/scripts/backup.sh > /dev/null 2>&1") | crontab -

echo "Cron jobs installed:"
crontab -l | grep partle
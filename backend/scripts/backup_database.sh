#!/bin/bash

# PostgreSQL Backup Script for Partle
# Runs daily backups with rotation (keeps last 7 days)

set -e

# Configuration
BACKUP_DIR="/srv/partle/backend/backups"
DB_NAME="partle"
DB_USER="partle_user"
DB_HOST="localhost"
LOG_FILE="$BACKUP_DIR/backup.log"
KEEP_DAYS=7

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Start backup
log_message "Starting PostgreSQL backup..."

# Use .pgpass file for secure authentication (no password in script)

# Perform backup
if pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" > "$BACKUP_FILE"; then
    # Compress the backup
    gzip "$BACKUP_FILE"
    BACKUP_FILE="$BACKUP_FILE.gz"
    
    # Get file size
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    
    log_message "Backup completed successfully: $(basename "$BACKUP_FILE") ($BACKUP_SIZE)"
    
    # Clean up old backups (keep only last KEEP_DAYS days)
    log_message "Cleaning up backups older than $KEEP_DAYS days..."
    find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -mtime +$KEEP_DAYS -delete
    
    # Count remaining backups
    BACKUP_COUNT=$(find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f | wc -l)
    log_message "Cleanup completed. $BACKUP_COUNT backup files remaining."
    
else
    log_message "ERROR: Backup failed!"
    exit 1
fi

# Unset password
unset PGPASSWORD

log_message "Backup process completed successfully."
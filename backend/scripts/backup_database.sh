#!/bin/bash

# PostgreSQL Backup Script for Partle
# Runs daily backups with rotation (keeps last 7 days)

set -e

# Load environment variables from .env file
if [ -f "/srv/partle/.env" ]; then
    export $(grep -v '^#' /srv/partle/.env | xargs)
fi

# Parse DATABASE_URL to extract components
# Format: postgresql://user:password@host:port/database
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL not found in environment"
    exit 1
fi

# Extract components from DATABASE_URL
DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
DB_PASSWORD=$(echo $DATABASE_URL | sed -n 's/.*:\/\/[^:]*:\([^@]*\)@.*/\1/p')
DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')

# Configuration
BACKUP_DIR="/srv/partle/backups"
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

# Set PGPASSWORD environment variable for pg_dump
export PGPASSWORD="$DB_PASSWORD"

# Perform backup
if pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" > "$BACKUP_FILE"; then
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

# Additional backup to debian laptop with retry logic
log_message "Starting backup transfer to debian laptop..."

# Retry configuration for Cloudflare Tunnel flakiness and router reboots
MAX_RETRIES=8
RETRY_DELAY=30
TRANSFER_SUCCESS=false

# Function to attempt SSH/SCP with timeout (2 minutes for large transfers)
try_ssh_command() {
    timeout 120 bash -c "$1"
    return $?
}

# Retry loop for creating remote directory
for attempt in $(seq 1 $MAX_RETRIES); do
    log_message "Attempt $attempt/$MAX_RETRIES: Creating remote backup directory..."

    if try_ssh_command "ssh debian 'mkdir -p ~/backups/partle'"; then
        log_message "Remote backup directory created/verified on debian laptop"
        break
    else
        if [ $attempt -lt $MAX_RETRIES ]; then
            log_message "Failed to connect to debian laptop, retrying in ${RETRY_DELAY}s..."
            sleep $RETRY_DELAY
            # Exponential backoff: double the delay each time
            RETRY_DELAY=$((RETRY_DELAY * 2))
        else
            log_message "ERROR: Failed to create remote backup directory after $MAX_RETRIES attempts"
            log_message "Backup process completed (local backup successful, remote backup failed)."
            exit 0
        fi
    fi
done

# Reset retry delay for SCP
RETRY_DELAY=10

# Retry loop for file transfer
for attempt in $(seq 1 $MAX_RETRIES); do
    log_message "Attempt $attempt/$MAX_RETRIES: Transferring backup file..."

    if try_ssh_command "scp '$BACKUP_FILE' debian:~/backups/partle/"; then
        log_message "Backup successfully transferred to debian laptop: $(basename "$BACKUP_FILE")"
        TRANSFER_SUCCESS=true
        break
    else
        if [ $attempt -lt $MAX_RETRIES ]; then
            log_message "Transfer failed, retrying in ${RETRY_DELAY}s..."
            sleep $RETRY_DELAY
            RETRY_DELAY=$((RETRY_DELAY * 2))
        else
            log_message "ERROR: Failed to transfer backup after $MAX_RETRIES attempts"
            log_message "Backup process completed (local backup successful, remote backup failed)."
            exit 0
        fi
    fi
done

# Only proceed with cleanup if transfer succeeded
if [ "$TRANSFER_SUCCESS" = true ]; then
    # Clean up old backups on debian laptop (keep only last KEEP_DAYS days)
    log_message "Cleaning up old backups on debian laptop..."

    if try_ssh_command "ssh debian 'find ~/backups/partle -name \"backup_*.sql.gz\" -type f -mtime +$KEEP_DAYS -delete'"; then
        # Count remaining backups on debian laptop
        REMOTE_BACKUP_COUNT=$(try_ssh_command "ssh debian 'find ~/backups/partle -name \"backup_*.sql.gz\" -type f | wc -l'")
        log_message "Remote cleanup completed. $REMOTE_BACKUP_COUNT backup files on debian laptop."
    else
        log_message "WARNING: Remote cleanup failed (backup still transferred successfully)"
    fi
fi

log_message "Backup process with remote copy completed."
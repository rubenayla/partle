#!/bin/bash
# Safe migration runner - always asks for confirmation

set -e  # Exit on error

echo "🔍 Migration Runner"
echo "==================="

# Check if .env exists
if [ -f ".env" ]; then
    # Extract database info for display (hiding password)
    DB_INFO=$(grep DATABASE_URL .env | sed 's/:[^:]*@/:****@/')
    echo "Found .env with: $DB_INFO"
    echo ""
    echo "⚠️  WARNING: This will run migrations against the database above!"
    echo -n "Are you sure? (yes/no): "
    read CONFIRM

    if [ "$CONFIRM" != "yes" ]; then
        echo "❌ Migration cancelled"
        exit 1
    fi

    # Load DATABASE_URL and run migration
    export $(grep DATABASE_URL .env)
    uv run alembic upgrade head
else
    echo "❌ No .env file found"
    echo ""
    echo "To run migrations, create a .env file with:"
    echo "DATABASE_URL=postgresql://user:pass@host/db"
    exit 1
fi
#!/bin/bash
# Debug wrapper for MCP servers

LOG_FILE="/tmp/mcp_debug_$(date +%Y%m%d_%H%M%S).log"

echo "=== MCP Debug Wrapper Started ===" >> $LOG_FILE
echo "Date: $(date)" >> $LOG_FILE
echo "PWD: $(pwd)" >> $LOG_FILE
echo "Script: $1" >> $LOG_FILE
echo "ENV vars:" >> $LOG_FILE
env | grep -E "PARTLE|DATABASE" >> $LOG_FILE 2>&1
echo "=== Starting MCP Server ===" >> $LOG_FILE

# Load .env file
if [ -f "../.env" ]; then
    echo "Loading ../.env" >> $LOG_FILE
    export $(grep -v '^#' ../.env | xargs)
fi

# Run the actual MCP server and log everything
exec poetry run python "$@" 2>> $LOG_FILE
#!/bin/bash
# MCP Server wrapper script that ensures environment is loaded

# Load environment variables from parent .env
if [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
fi

# Run the MCP server script passed as argument
exec poetry run python "$@"
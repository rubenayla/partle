#!/usr/bin/env python3
"""Launch script for Partle Scraper Monitor MCP Server."""
import sys
import os
import logging
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.scraper_monitor import mcp_server
from mcp.server.stdio import stdio_server


async def main():
    """Run the Partle Scraper Monitor MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)
    logger.info('Starting Partle Scraper Monitor MCP Server...')

    try:
        # Run the MCP server using stdio
        async with stdio_server() as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options()
            )
    except KeyboardInterrupt:
        logger.info('Server stopped by user')
    except Exception as e:
        logger.error(f'Server error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
#!/usr/bin/env python3
"""Launch script for Partle Analytics MCP Server."""
import sys
import os
import logging

# Add the backend app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.mcp.analytics import mcp_server


def main():
    """Run the Partle Analytics MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info('Starting Partle Analytics MCP Server...')
    
    try:
        # Run the MCP server
        mcp_server.run()
    except KeyboardInterrupt:
        logger.info('Server stopped by user')
    except Exception as e:
        logger.error(f'Server error: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
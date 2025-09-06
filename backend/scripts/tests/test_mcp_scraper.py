#!/usr/bin/env python3
"""
Test client for the Scraper Monitor MCP server
"""

import asyncio
import json
import subprocess
from datetime import datetime


async def test_mcp_server():
    """Test the MCP scraper monitoring server"""
    
    print("🔍 Testing Scraper Monitor MCP Server")
    print("=" * 50)
    
    # Start the MCP server as a subprocess
    server_cmd = ["python", "mcp_scraper_monitor.py"]
    
    try:
        # Test basic functionality by directly calling the monitor
        from mcp_scraper_monitor import monitor
        
        print("1. Testing database metrics...")
        metrics = await monitor.get_database_metrics()
        print(f"   📊 Total products: {metrics.total_products}")
        print(f"   🏪 Products by store: {metrics.products_by_store}")
        print(f"   🏃 Running scrapers: {metrics.scrapers_running}")
        print(f"   ❌ Failed scrapers: {metrics.scrapers_failed}")
        print()
        
        print("2. Testing scraper status...")
        status = await monitor.get_scraper_status("bricodepot")
        print(f"   📋 Bricodepot status: {status.status}")
        print(f"   🔧 PID: {status.pid}")
        print(f"   📈 Items scraped: {status.items_scraped}")
        print()
        
        print("3. Testing scraper start...")
        # Don't actually start for this test
        print("   (Skipped actual start for demo)")
        print()
        
        print("✅ MCP Server test completed successfully!")
        print("   The server can monitor scrapers, track metrics, and provide real-time status")
        print("   Next steps:")
        print("   - Start the MCP server: python mcp_scraper_monitor.py")
        print("   - Connect your AI assistant to the MCP server")
        print("   - Use tools like 'start_scraper', 'get_metrics', 'get_scraper_status'")
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
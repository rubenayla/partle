#!/usr/bin/env python3
"""
MCP Server for Scraper Monitoring and Management
Provides real-time monitoring, control, and analytics for web scrapers.
"""

import asyncio
import json
import subprocess
import psutil
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from sqlalchemy import create_engine, text
import mcp.types as types
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from dotenv import load_dotenv

# Load environment variables from root .env
root_env = Path(__file__).parent.parent / '.env'
load_dotenv(root_env)


@dataclass
class ScraperStatus:
    """Current status of a scraper"""
    name: str
    pid: Optional[int]
    status: str  # running, stopped, failed, completed
    start_time: Optional[datetime]
    runtime_seconds: Optional[int]
    pages_crawled: int
    items_scraped: int
    current_rate: float  # items per minute
    errors: List[str]
    memory_usage: Optional[int]  # MB
    last_activity: Optional[datetime]


@dataclass
class ScrapingMetrics:
    """Overall scraping metrics"""
    total_products: int
    products_by_store: Dict[str, int]
    scrapers_running: int
    scrapers_failed: int
    total_runtime: int
    avg_scrape_rate: float


class ScraperMonitor:
    """Monitors and manages web scrapers"""
    
    def __init__(self):
        self.scrapers: Dict[str, ScraperStatus] = {}
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL environment variable is required")
        self.engine = create_engine(self.db_url)
        self.scraper_processes: Dict[str, subprocess.Popen] = {}
        
    async def get_scraper_status(self, scraper_name: str) -> ScraperStatus:
        """Get current status of a specific scraper"""
        if scraper_name not in self.scrapers:
            self.scrapers[scraper_name] = ScraperStatus(
                name=scraper_name,
                pid=None,
                status="stopped",
                start_time=None,
                runtime_seconds=0,
                pages_crawled=0,
                items_scraped=0,
                current_rate=0.0,
                errors=[],
                memory_usage=None,
                last_activity=None
            )
        return self.scrapers[scraper_name]
    
    async def start_scraper(self, scraper_name: str) -> Dict[str, Any]:
        """Start a scraper and begin monitoring"""
        try:
            # Start the scraper process
            cmd = [
                "poetry", "run", "scrapy", "crawl", scraper_name, "-L", "INFO"
            ]
            
            # Change to scraper directory
            scraper_dir = Path("/home/rubenayla/repos/partle/backend/app/scraper/store_scrapers")
            
            process = subprocess.Popen(
                cmd,
                cwd=scraper_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.scraper_processes[scraper_name] = process
            
            # Update status
            status = await self.get_scraper_status(scraper_name)
            status.pid = process.pid
            status.status = "running"
            status.start_time = datetime.now()
            status.errors = []
            
            return {
                "success": True,
                "message": f"Started scraper {scraper_name}",
                "pid": process.pid
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to start scraper {scraper_name}: {str(e)}"
            }
    
    async def stop_scraper(self, scraper_name: str) -> Dict[str, Any]:
        """Stop a running scraper"""
        try:
            if scraper_name in self.scraper_processes:
                process = self.scraper_processes[scraper_name]
                process.terminate()
                process.wait(timeout=10)
                del self.scraper_processes[scraper_name]
                
                # Update status
                status = await self.get_scraper_status(scraper_name)
                status.status = "stopped"
                status.pid = None
                
                return {
                    "success": True,
                    "message": f"Stopped scraper {scraper_name}"
                }
            else:
                return {
                    "success": False,
                    "message": f"Scraper {scraper_name} is not running"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to stop scraper {scraper_name}: {str(e)}"
            }
    
    async def get_database_metrics(self) -> ScrapingMetrics:
        """Get current database metrics"""
        try:
            with self.engine.connect() as conn:
                # Total products
                total = conn.execute(text('SELECT COUNT(*) FROM products')).scalar()
                
                # Products by store
                result = conn.execute(text('''
                    SELECT store_id, COUNT(*) as count 
                    FROM products 
                    GROUP BY store_id 
                    ORDER BY count DESC
                '''))
                products_by_store = {str(row.store_id): row.count for row in result}
                
                # Scraper stats
                running_scrapers = len([s for s in self.scrapers.values() if s.status == "running"])
                failed_scrapers = len([s for s in self.scrapers.values() if s.status == "failed"])
                
                # Calculate rates
                total_runtime = sum(s.runtime_seconds or 0 for s in self.scrapers.values())
                avg_rate = (total / (total_runtime / 60)) if total_runtime > 0 else 0
                
                return ScrapingMetrics(
                    total_products=total,
                    products_by_store=products_by_store,
                    scrapers_running=running_scrapers,
                    scrapers_failed=failed_scrapers,
                    total_runtime=total_runtime,
                    avg_scrape_rate=avg_rate
                )
                
        except Exception as e:
            return ScrapingMetrics(
                total_products=0,
                products_by_store={},
                scrapers_running=0,
                scrapers_failed=0,
                total_runtime=0,
                avg_scrape_rate=0.0
            )
    
    async def update_scraper_status(self, scraper_name: str):
        """Update scraper status from process info and logs"""
        if scraper_name not in self.scraper_processes:
            return
            
        process = self.scraper_processes[scraper_name]
        status = await self.get_scraper_status(scraper_name)
        
        # Check if process is still running
        if process.poll() is not None:
            status.status = "completed" if process.returncode == 0 else "failed"
            status.pid = None
            del self.scraper_processes[scraper_name]
            return
        
        # Update runtime
        if status.start_time:
            status.runtime_seconds = int((datetime.now() - status.start_time).total_seconds())
        
        # Get memory usage
        try:
            ps_process = psutil.Process(process.pid)
            status.memory_usage = int(ps_process.memory_info().rss / 1024 / 1024)  # MB
        except:
            status.memory_usage = None
        
        # Parse logs for metrics (simplified - would need real log parsing)
        status.last_activity = datetime.now()
    
    async def monitor_loop(self):
        """Continuous monitoring loop"""
        while True:
            try:
                for scraper_name in list(self.scrapers.keys()):
                    await self.update_scraper_status(scraper_name)
                    
                await asyncio.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"Monitor loop error: {e}")
                await asyncio.sleep(10)


# Initialize monitor
monitor = ScraperMonitor()

# Create MCP server
server = Server("scraper-monitor")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available scraper monitoring tools"""
    return [
        types.Tool(
            name="start_scraper",
            description="Start a web scraper",
            inputSchema={
                "type": "object",
                "properties": {
                    "scraper_name": {
                        "type": "string",
                        "description": "Name of the scraper to start (e.g., 'bricodepot', 'leroy')"
                    }
                },
                "required": ["scraper_name"]
            }
        ),
        types.Tool(
            name="stop_scraper", 
            description="Stop a running scraper",
            inputSchema={
                "type": "object",
                "properties": {
                    "scraper_name": {
                        "type": "string",
                        "description": "Name of the scraper to stop"
                    }
                },
                "required": ["scraper_name"]
            }
        ),
        types.Tool(
            name="get_scraper_status",
            description="Get detailed status of a specific scraper",
            inputSchema={
                "type": "object", 
                "properties": {
                    "scraper_name": {
                        "type": "string",
                        "description": "Name of the scraper to check"
                    }
                },
                "required": ["scraper_name"]
            }
        ),
        types.Tool(
            name="get_all_scrapers",
            description="Get status of all scrapers",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="get_metrics",
            description="Get overall scraping metrics and database stats",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="restart_failed_scrapers",
            description="Restart any failed scrapers",
            inputSchema={"type": "object", "properties": {}}
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool calls"""
    args = arguments or {}
    
    if name == "start_scraper":
        result = await monitor.start_scraper(args["scraper_name"])
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "stop_scraper":
        result = await monitor.stop_scraper(args["scraper_name"]) 
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_scraper_status":
        status = await monitor.get_scraper_status(args["scraper_name"])
        result = asdict(status)
        # Convert datetime objects to strings
        if result["start_time"]:
            result["start_time"] = result["start_time"].isoformat()
        if result["last_activity"]:
            result["last_activity"] = result["last_activity"].isoformat()
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_all_scrapers":
        all_scrapers = {}
        for scraper_name, status in monitor.scrapers.items():
            status_dict = asdict(status)
            if status_dict["start_time"]:
                status_dict["start_time"] = status_dict["start_time"].isoformat()
            if status_dict["last_activity"]:
                status_dict["last_activity"] = status_dict["last_activity"].isoformat()
            all_scrapers[scraper_name] = status_dict
        return [types.TextContent(type="text", text=json.dumps(all_scrapers, indent=2))]
    
    elif name == "get_metrics":
        metrics = await monitor.get_database_metrics()
        result = asdict(metrics)
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "restart_failed_scrapers":
        results = []
        for scraper_name, status in monitor.scrapers.items():
            if status.status == "failed":
                result = await monitor.start_scraper(scraper_name)
                results.append(f"{scraper_name}: {result['message']}")
        
        return [types.TextContent(type="text", text=json.dumps({
            "restarted": results
        }, indent=2))]
    
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Run the MCP server with monitoring loop"""
    # Start monitoring loop in background
    monitor_task = asyncio.create_task(monitor.monitor_loop())
    
    # Run MCP server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="scraper-monitor",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
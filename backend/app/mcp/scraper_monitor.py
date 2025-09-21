"""MCP Server for Partle Scraper Management and Monitoring."""
import logging
import json
import subprocess
import asyncio
import os
from typing import Optional, Any, Dict, List
from datetime import datetime, timedelta
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
from sqlalchemy import create_engine, text
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
API_BASE_URL = os.getenv('PARTLE_API_URL', 'http://localhost:8000')
DATABASE_URL = os.getenv('DATABASE_URL')

# Initialize MCP server
mcp_server = Server('partle-scraper-monitor')

# Track running scrapers
RUNNING_SCRAPERS: Dict[str, subprocess.Popen] = {}
SCRAPER_LOGS: Dict[str, List[str]] = {}


def get_scraper_base_path() -> Path:
    """Get the base path for scrapers."""
    return Path(__file__).parent.parent / 'scraper'


def get_available_scrapers() -> List[Dict[str, Any]]:
    """Get list of available scrapers with their configuration."""
    scraper_path = get_scraper_base_path() / 'store_scrapers' / 'spiders'
    scrapers = []

    # Map of scraper names to their descriptions and URLs
    scraper_info = {
        'bricodepot': {
            'name': 'Brico Depot',
            'url': 'https://www.bricodepot.es',
            'category': 'Hardware/DIY',
            'description': 'Spanish DIY and construction materials retailer'
        },
        'bricodepot_simple': {
            'name': 'Brico Depot (Simple)',
            'url': 'https://www.bricodepot.es',
            'category': 'Hardware/DIY',
            'description': 'Simplified Brico Depot scraper for specific categories'
        },
        'leroy_merlin': {
            'name': 'Leroy Merlin',
            'url': 'https://www.leroymerlin.es',
            'category': 'Hardware/DIY',
            'description': 'Major European home improvement and gardening retailer'
        },
        'bauhaus': {
            'name': 'Bauhaus',
            'url': 'https://www.bauhaus.es',
            'category': 'Hardware/DIY',
            'description': 'German DIY and building materials chain'
        },
        'ferreterias': {
            'name': 'Ferreterías',
            'url': 'Various',
            'category': 'Hardware',
            'description': 'Multiple Spanish hardware stores'
        },
        'ferreteria_shop': {
            'name': 'Ferreteria Shop',
            'url': 'https://www.ferreteria.shop',
            'category': 'Hardware',
            'description': 'Online hardware store'
        },
        'mengual': {
            'name': 'Mengual',
            'url': 'https://www.mengual.es',
            'category': 'Industrial/Tools',
            'description': 'Industrial supplies and tools'
        },
        'mengual_simple': {
            'name': 'Mengual (Simple)',
            'url': 'https://www.mengual.es',
            'category': 'Industrial/Tools',
            'description': 'Simplified Mengual scraper'
        },
        'mengual_bulk': {
            'name': 'Mengual (Bulk)',
            'url': 'https://www.mengual.es',
            'category': 'Industrial/Tools',
            'description': 'Bulk product scraper for Mengual'
        },
        'carrefour': {
            'name': 'Carrefour',
            'url': 'https://www.carrefour.es',
            'category': 'Supermarket/General',
            'description': 'French multinational retail corporation'
        },
        'rationalstock': {
            'name': 'Rational Stock',
            'url': 'https://www.rationalstock.es',
            'category': 'Electronics/Tech',
            'description': 'Electronics and technology products'
        },
        'rationalstock_simple': {
            'name': 'Rational Stock (Simple)',
            'url': 'https://www.rationalstock.es',
            'category': 'Electronics/Tech',
            'description': 'Simplified version for specific categories'
        },
        'products_direct': {
            'name': 'Products Direct',
            'url': 'https://www.products-direct.es',
            'category': 'General',
            'description': 'Direct product imports and sales'
        }
    }

    if scraper_path.exists():
        for spider_file in scraper_path.glob('*.py'):
            if spider_file.name != '__init__.py':
                spider_name = spider_file.stem
                info = scraper_info.get(spider_name, {})
                scrapers.append({
                    'spider_name': spider_name,
                    'file_path': str(spider_file),
                    'name': info.get('name', spider_name.replace('_', ' ').title()),
                    'url': info.get('url', 'Unknown'),
                    'category': info.get('category', 'General'),
                    'description': info.get('description', 'Product scraper'),
                    'status': 'running' if spider_name in RUNNING_SCRAPERS else 'stopped'
                })

    return scrapers


def get_scraper_stats() -> Dict[str, Any]:
    """Get statistics about scraped products from database."""
    if not DATABASE_URL:
        return {'error': 'DATABASE_URL not configured'}

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Total products
            total_products = conn.execute(
                text("SELECT COUNT(*) FROM products")
            ).scalar()

            # Products by store
            products_by_store = conn.execute(
                text("""
                    SELECT s.name, COUNT(p.id) as product_count
                    FROM stores s
                    LEFT JOIN products p ON s.id = p.store_id
                    GROUP BY s.id, s.name
                    ORDER BY product_count DESC
                    LIMIT 20
                """)
            ).fetchall()

            # Recent scraping activity
            recent_products = conn.execute(
                text("""
                    SELECT COUNT(*) as count
                    FROM products
                    WHERE created_at > NOW() - INTERVAL '24 hours'
                """)
            ).scalar()

            # Get scrapers with most recent activity
            recent_activity = conn.execute(
                text("""
                    SELECT s.name as store_name,
                           MAX(p.created_at) as last_scraped,
                           COUNT(CASE WHEN p.created_at > NOW() - INTERVAL '24 hours'
                                 THEN 1 END) as products_24h
                    FROM stores s
                    LEFT JOIN products p ON s.id = p.store_id
                    GROUP BY s.id, s.name
                    HAVING MAX(p.created_at) IS NOT NULL
                    ORDER BY last_scraped DESC
                    LIMIT 10
                """)
            ).fetchall()

            return {
                'total_products': total_products,
                'products_by_store': [
                    {'store': row.name, 'count': row.product_count}
                    for row in products_by_store
                ],
                'products_last_24h': recent_products,
                'recent_activity': [
                    {
                        'store': row.store_name,
                        'last_scraped': row.last_scraped.isoformat() if row.last_scraped else None,
                        'products_24h': row.products_24h
                    }
                    for row in recent_activity
                ]
            }
    except Exception as e:
        logger.error(f"Error getting scraper stats: {e}")
        return {'error': str(e)}


async def start_scraper(spider_name: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
    """Start a scraper process."""
    if spider_name in RUNNING_SCRAPERS:
        return {
            'success': False,
            'message': f'Scraper {spider_name} is already running'
        }

    try:
        scraper_path = get_scraper_base_path()

        # Build command
        cmd = [
            'uv', 'run', 'python', 'run_spider.py', spider_name
        ]

        # Add options
        if options:
            if options.get('debug'):
                cmd.extend(['--log-level', 'DEBUG'])
            if options.get('no_resume'):
                cmd.append('--no-resume')
            if options.get('dry_run'):
                cmd.append('--dry-run')

        # Start the process
        process = subprocess.Popen(
            cmd,
            cwd=scraper_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        RUNNING_SCRAPERS[spider_name] = process
        SCRAPER_LOGS[spider_name] = []

        # Start monitoring the output
        asyncio.create_task(monitor_scraper_output(spider_name, process))

        return {
            'success': True,
            'message': f'Started scraper {spider_name}',
            'pid': process.pid
        }
    except Exception as e:
        logger.error(f"Failed to start scraper {spider_name}: {e}")
        return {
            'success': False,
            'message': f'Failed to start scraper: {str(e)}'
        }


async def monitor_scraper_output(spider_name: str, process: subprocess.Popen):
    """Monitor scraper output and store logs."""
    try:
        for line in iter(process.stdout.readline, ''):
            if not line:
                break
            SCRAPER_LOGS[spider_name].append(line.strip())
            # Keep only last 1000 lines
            if len(SCRAPER_LOGS[spider_name]) > 1000:
                SCRAPER_LOGS[spider_name] = SCRAPER_LOGS[spider_name][-1000:]
    except Exception as e:
        logger.error(f"Error monitoring scraper {spider_name}: {e}")
    finally:
        # Clean up when process ends
        if spider_name in RUNNING_SCRAPERS:
            del RUNNING_SCRAPERS[spider_name]


async def stop_scraper(spider_name: str) -> Dict[str, Any]:
    """Stop a running scraper."""
    if spider_name not in RUNNING_SCRAPERS:
        return {
            'success': False,
            'message': f'Scraper {spider_name} is not running'
        }

    try:
        process = RUNNING_SCRAPERS[spider_name]
        process.terminate()

        # Wait for process to end
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

        del RUNNING_SCRAPERS[spider_name]

        return {
            'success': True,
            'message': f'Stopped scraper {spider_name}'
        }
    except Exception as e:
        logger.error(f"Failed to stop scraper {spider_name}: {e}")
        return {
            'success': False,
            'message': f'Failed to stop scraper: {str(e)}'
        }


def get_scraper_logs(spider_name: str, lines: int = 50) -> List[str]:
    """Get recent logs for a scraper."""
    if spider_name in SCRAPER_LOGS:
        return SCRAPER_LOGS[spider_name][-lines:]

    # Try to get logs from file
    log_path = get_scraper_base_path() / 'logs'
    if log_path.exists():
        # Find most recent log file for this scraper
        log_files = sorted(log_path.glob(f'*{spider_name}*.log'), key=lambda p: p.stat().st_mtime, reverse=True)
        if log_files:
            try:
                with open(log_files[0], 'r') as f:
                    all_lines = f.readlines()
                    return [line.strip() for line in all_lines[-lines:]]
            except Exception as e:
                logger.error(f"Failed to read log file: {e}")

    return []


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List available scraper management tools."""
    return [
        Tool(
            name='list_scrapers',
            description='List all available scrapers with their status and information',
            inputSchema={'type': 'object', 'properties': {}}
        ),
        Tool(
            name='start_scraper',
            description='Start a web scraper to collect products from a specific website',
            inputSchema={
                'type': 'object',
                'properties': {
                    'spider_name': {
                        'type': 'string',
                        'description': 'Name of the scraper/spider to start (e.g., bricodepot, leroy_merlin)'
                    },
                    'debug': {
                        'type': 'boolean',
                        'default': False,
                        'description': 'Enable debug logging'
                    },
                    'no_resume': {
                        'type': 'boolean',
                        'default': False,
                        'description': 'Start fresh instead of resuming from last position'
                    },
                    'dry_run': {
                        'type': 'boolean',
                        'default': False,
                        'description': 'Run without saving to database (test mode)'
                    }
                },
                'required': ['spider_name']
            }
        ),
        Tool(
            name='stop_scraper',
            description='Stop a running scraper',
            inputSchema={
                'type': 'object',
                'properties': {
                    'spider_name': {
                        'type': 'string',
                        'description': 'Name of the scraper to stop'
                    }
                },
                'required': ['spider_name']
            }
        ),
        Tool(
            name='get_scraper_status',
            description='Get the current status and logs of a specific scraper',
            inputSchema={
                'type': 'object',
                'properties': {
                    'spider_name': {
                        'type': 'string',
                        'description': 'Name of the scraper to check'
                    },
                    'log_lines': {
                        'type': 'integer',
                        'default': 50,
                        'description': 'Number of recent log lines to return'
                    }
                },
                'required': ['spider_name']
            }
        ),
        Tool(
            name='get_scraper_stats',
            description='Get statistics about scraped products and recent activity',
            inputSchema={'type': 'object', 'properties': {}}
        ),
        Tool(
            name='bulk_start_scrapers',
            description='Start multiple scrapers at once',
            inputSchema={
                'type': 'object',
                'properties': {
                    'spider_names': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'List of scraper names to start'
                    },
                    'stagger_seconds': {
                        'type': 'integer',
                        'default': 30,
                        'description': 'Seconds to wait between starting each scraper'
                    }
                },
                'required': ['spider_names']
            }
        ),
        Tool(
            name='stop_all_scrapers',
            description='Stop all running scrapers',
            inputSchema={'type': 'object', 'properties': {}}
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> List[TextContent]:
    """Handle tool calls for scraper management."""
    try:
        if name == 'list_scrapers':
            scrapers = get_available_scrapers()
            running_count = len(RUNNING_SCRAPERS)

            result = f"Found {len(scrapers)} scrapers ({running_count} running):\n\n"

            # Group by category
            by_category = {}
            for scraper in scrapers:
                cat = scraper['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(scraper)

            for category, items in sorted(by_category.items()):
                result += f"**{category}:**\n"
                for scraper in items:
                    status_icon = '🟢' if scraper['status'] == 'running' else '⚫'
                    result += f"{status_icon} **{scraper['spider_name']}** - {scraper['name']}\n"
                    result += f"   URL: {scraper['url']}\n"
                    result += f"   {scraper['description']}\n\n"

            return [TextContent(type='text', text=result)]

        elif name == 'start_scraper':
            spider_name = arguments['spider_name']
            options = {k: v for k, v in arguments.items() if k != 'spider_name'}
            result = await start_scraper(spider_name, options)

            if result['success']:
                return [TextContent(
                    type='text',
                    text=f"✅ {result['message']} (PID: {result.get('pid', 'unknown')})"
                )]
            else:
                return [TextContent(type='text', text=f"❌ {result['message']}")]

        elif name == 'stop_scraper':
            result = await stop_scraper(arguments['spider_name'])
            if result['success']:
                return [TextContent(type='text', text=f"✅ {result['message']}")]
            else:
                return [TextContent(type='text', text=f"❌ {result['message']}")]

        elif name == 'get_scraper_status':
            spider_name = arguments['spider_name']
            log_lines = arguments.get('log_lines', 50)

            is_running = spider_name in RUNNING_SCRAPERS
            logs = get_scraper_logs(spider_name, log_lines)

            status_text = f"**Scraper: {spider_name}**\n"
            status_text += f"Status: {'🟢 Running' if is_running else '⚫ Stopped'}\n"

            if is_running:
                process = RUNNING_SCRAPERS[spider_name]
                status_text += f"PID: {process.pid}\n"

            if logs:
                status_text += f"\n**Recent logs ({len(logs)} lines):**\n```\n"
                status_text += '\n'.join(logs[-20:])  # Show last 20 lines
                status_text += "\n```"
            else:
                status_text += "\nNo recent logs available."

            return [TextContent(type='text', text=status_text)]

        elif name == 'get_scraper_stats':
            stats = get_scraper_stats()

            if 'error' in stats:
                return [TextContent(type='text', text=f"❌ Error: {stats['error']}")]

            result = "**Scraping Statistics:**\n\n"
            result += f"📊 **Total Products:** {stats['total_products']:,}\n"
            result += f"⏱️ **Products (last 24h):** {stats['products_last_24h']:,}\n\n"

            result += "**Products by Store (Top 10):**\n"
            for item in stats['products_by_store'][:10]:
                result += f"• {item['store']}: {item['count']:,} products\n"

            result += "\n**Recent Activity:**\n"
            for activity in stats['recent_activity']:
                result += f"• {activity['store']}: "
                result += f"{activity['products_24h']} products in 24h, "
                result += f"last: {activity['last_scraped']}\n"

            return [TextContent(type='text', text=result)]

        elif name == 'bulk_start_scrapers':
            spider_names = arguments['spider_names']
            stagger = arguments.get('stagger_seconds', 30)

            results = []
            for spider_name in spider_names:
                result = await start_scraper(spider_name)
                results.append(f"{spider_name}: {'✅ Started' if result['success'] else '❌ ' + result['message']}")

                if stagger > 0 and spider_name != spider_names[-1]:
                    await asyncio.sleep(stagger)

            return [TextContent(type='text', text='\n'.join(results))]

        elif name == 'stop_all_scrapers':
            if not RUNNING_SCRAPERS:
                return [TextContent(type='text', text='No scrapers are currently running.')]

            results = []
            for spider_name in list(RUNNING_SCRAPERS.keys()):
                result = await stop_scraper(spider_name)
                results.append(f"{spider_name}: {'✅ Stopped' if result['success'] else '❌ Failed'}")

            return [TextContent(type='text', text='\n'.join(results))]

        else:
            return [TextContent(type='text', text=f'Unknown tool: {name}')]

    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [TextContent(type='text', text=f'Error: {str(e)}')]


def create_initialization_options():
    """Create initialization options for the MCP server."""
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions
    return InitializationOptions(
        server_name='partle-scraper-monitor',
        server_version='1.0.0',
        capabilities=mcp_server.get_capabilities(
            notification_options=NotificationOptions(),
            experimental_capabilities={},
        )
    )
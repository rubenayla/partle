"""MCP Server for Partle Stores API integration."""
import logging
from typing import Optional, Any, Dict, List
from contextlib import contextmanager
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
API_BASE_URL = os.getenv('PARTLE_API_URL', 'http://localhost:8000')

# Initialize MCP server
mcp_server = Server('partle-stores')


@contextmanager
def get_http_client():
    """Get HTTP client for API requests."""
    with httpx.Client(base_url=API_BASE_URL) as client:
        yield client


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for stores management."""
    return [
        Tool(
            name='search_stores',
            description='Search and filter stores by name, address, homepage, and tags',
            inputSchema={
                'type': 'object',
                'properties': {
                    'q': {
                        'type': 'string',
                        'description': 'Search query for store name, address, or homepage'
                    },
                    'tags': {
                        'type': 'string',
                        'description': 'Comma-separated list of tags to filter by'
                    },
                    'sort_by': {
                        'type': 'string',
                        'enum': ['created_at', 'created_at_asc', 'random'],
                        'description': 'Sort order for results'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 20,
                        'description': 'Maximum number of results to return'
                    },
                    'offset': {
                        'type': 'integer',
                        'default': 0,
                        'description': 'Number of results to skip for pagination'
                    }
                }
            }
        ),
        Tool(
            name='get_store',
            description='Get detailed information about a specific store by ID',
            inputSchema={
                'type': 'object',
                'properties': {
                    'store_id': {
                        'type': 'integer',
                        'description': 'The ID of the store to retrieve'
                    }
                },
                'required': ['store_id']
            }
        ),
        Tool(
            name='list_stores_dropdown',
            description='Get a simplified list of all stores (ID and name only) for dropdown/selection purposes',
            inputSchema={
                'type': 'object',
                'properties': {}
            }
        ),
        Tool(
            name='get_store_analytics',
            description='Get analytical information about a store including product count and price statistics',
            inputSchema={
                'type': 'object',
                'properties': {
                    'store_id': {
                        'type': 'integer',
                        'description': 'The ID of the store to analyze'
                    }
                },
                'required': ['store_id']
            }
        },
        Tool(
            name='find_stores_by_type',
            description='Find stores by their type (physical, online, or chain)',
            inputSchema={
                'type': 'object',
                'properties': {
                    'store_type': {
                        'type': 'string',
                        'enum': ['physical', 'online', 'chain'],
                        'description': 'Type of store to search for'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 20,
                        'description': 'Maximum number of results'
                    }
                },
                'required': ['store_type']
            }
        },
        Tool(
            name='find_stores_near_location',
            description='Find physical stores near a specific location (requires stores to have lat/lon coordinates)',
            inputSchema={
                'type': 'object',
                'properties': {
                    'lat': {
                        'type': 'number',
                        'description': 'Latitude coordinate'
                    },
                    'lon': {
                        'type': 'number',
                        'description': 'Longitude coordinate'
                    },
                    'radius_km': {
                        'type': 'number',
                        'default': 10,
                        'description': 'Search radius in kilometers'
                    }
                },
                'required': ['lat', 'lon']
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[TextContent]:
    """Handle tool calls for stores operations."""
    try:
        if name == 'search_stores':
            return await _search_stores(arguments or {})
        elif name == 'get_store':
            return await _get_store(arguments or {})
        elif name == 'list_stores_dropdown':
            return await _list_stores_dropdown(arguments or {})
        elif name == 'get_store_analytics':
            return await _get_store_analytics(arguments or {})
        elif name == 'find_stores_by_type':
            return await _find_stores_by_type(arguments or {})
        elif name == 'find_stores_near_location':
            return await _find_stores_near_location(arguments or {})
        else:
            return [TextContent(type='text', text=f'Unknown tool: {name}')]
    except Exception as e:
        logger.error(f'Error calling tool {name}: {e}')
        return [TextContent(type='text', text=f'Error: {str(e)}')]


async def _search_stores(args: Dict[str, Any]) -> List[TextContent]:
    """Search stores with various filters."""
    with get_http_client() as client:
        params = {k: v for k, v in args.items() if v is not None}
        response = client.get('/v1/stores/', params=params)
        response.raise_for_status()
        
        stores = response.json()
        if not stores:
            return [TextContent(type='text', text='No stores found matching your criteria.')]
        
        result = f'Found {len(stores)} stores:\\n\\n'
        for store in stores:
            result += f'**{store["name"]}** ({store["type"]})\\n'
            if store.get('address'):
                result += f'Address: {store["address"]}\\n'
            if store.get('homepage'):
                result += f'Website: {store["homepage"]}\\n'
            if store.get('tags'):
                tags = [tag['name'] for tag in store['tags']]
                result += f'Tags: {", ".join(tags)}\\n'
            result += f'ID: {store["id"]}\\n\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_store(args: Dict[str, Any]) -> List[TextContent]:
    """Get specific store details."""
    store_id = args.get('store_id')
    if not store_id:
        return [TextContent(type='text', text='Error: store_id is required')]
    
    with get_http_client() as client:
        response = client.get(f'/v1/stores/{store_id}')
        if response.status_code == 404:
            return [TextContent(type='text', text=f'Store with ID {store_id} not found.')]
        
        response.raise_for_status()
        store = response.json()
        
        result = f'**{store["name"]}**\\n\\n'
        result += f'**Type:** {store["type"].title()}\\n'
        
        if store.get('address'):
            result += f'**Address:** {store["address"]}\\n'
        if store.get('homepage'):
            result += f'**Website:** {store["homepage"]}\\n'
        if store.get('lat') and store.get('lon'):
            result += f'**Location:** {store["lat"]}, {store["lon"]}\\n'
        if store.get('owner'):
            result += f'**Owner:** {store["owner"]["email"]}\\n'
        if store.get('tags'):
            tags = [tag['name'] for tag in store['tags']]
            result += f'**Tags:** {", ".join(tags)}\\n'
        
        result += f'\\n**Store ID:** {store["id"]}\\n'
        
        return [TextContent(type='text', text=result)]


async def _list_stores_dropdown(args: Dict[str, Any]) -> List[TextContent]:
    """Get simplified store list for dropdown."""
    with get_http_client() as client:
        response = client.get('/v1/stores/dropdown')
        response.raise_for_status()
        
        stores = response.json()
        if not stores:
            return [TextContent(type='text', text='No stores available.')]
        
        result = f'Available stores ({len(stores)} total):\\n\\n'
        for store in stores:
            result += f'• {store["name"]} (ID: {store["id"]})\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_store_analytics(args: Dict[str, Any]) -> List[TextContent]:
    """Get analytics for a specific store."""
    store_id = args.get('store_id')
    if not store_id:
        return [TextContent(type='text', text='Error: store_id is required')]
    
    with get_http_client() as client:
        # First get store details
        store_response = client.get(f'/v1/stores/{store_id}')
        if store_response.status_code == 404:
            return [TextContent(type='text', text=f'Store with ID {store_id} not found.')]
        store_response.raise_for_status()
        store = store_response.json()
        
        # Get products for this store
        products_response = client.get(f'/v1/products/store/{store_id}')
        products_response.raise_for_status()
        products = products_response.json()
        
        result = f'**Analytics for {store["name"]}**\\n\\n'
        result += f'**Total Products:** {len(products)}\\n'
        
        if products:
            # Calculate price statistics
            prices = [p['price'] for p in products if p.get('price') is not None]
            if prices:
                result += f'**Products with Prices:** {len(prices)} of {len(products)}\\n'
                result += f'**Price Range:** €{min(prices):.2f} - €{max(prices):.2f}\\n'
                result += f'**Average Price:** €{sum(prices)/len(prices):.2f}\\n'
            else:
                result += f'**Products with Prices:** 0 of {len(products)}\\n'
            
            # Tag analysis
            all_tags = []
            for product in products:
                if product.get('tags'):
                    all_tags.extend([tag['name'] for tag in product['tags']])
            
            if all_tags:
                from collections import Counter
                tag_counts = Counter(all_tags)
                result += f'\\n**Most Common Product Tags:**\\n'
                for tag, count in tag_counts.most_common(5):
                    result += f'  • {tag}: {count} products\\n'
        else:
            result += 'This store has no products yet.\\n'
        
        return [TextContent(type='text', text=result)]


async def _find_stores_by_type(args: Dict[str, Any]) -> List[TextContent]:
    """Find stores by type."""
    store_type = args.get('store_type')
    limit = args.get('limit', 20)
    
    if not store_type:
        return [TextContent(type='text', text='Error: store_type is required')]
    
    with get_http_client() as client:
        response = client.get('/v1/stores/', params={'limit': limit})
        response.raise_for_status()
        
        all_stores = response.json()
        # Filter by type (API doesn't have type filter, so we filter client-side)
        filtered_stores = [s for s in all_stores if s.get('type') == store_type]
        
        if not filtered_stores:
            return [TextContent(type='text', text=f'No {store_type} stores found.')]
        
        result = f'Found {len(filtered_stores)} {store_type} stores:\\n\\n'
        for store in filtered_stores:
            result += f'**{store["name"]}**\\n'
            if store.get('address'):
                result += f'Address: {store["address"]}\\n'
            if store.get('homepage'):
                result += f'Website: {store["homepage"]}\\n'
            result += f'ID: {store["id"]}\\n\\n'
        
        return [TextContent(type='text', text=result)]


async def _find_stores_near_location(args: Dict[str, Any]) -> List[TextContent]:
    """Find stores near a location."""
    lat = args.get('lat')
    lon = args.get('lon')
    radius_km = args.get('radius_km', 10)
    
    if lat is None or lon is None:
        return [TextContent(type='text', text='Error: lat and lon are required')]
    
    with get_http_client() as client:
        response = client.get('/v1/stores/')
        response.raise_for_status()
        
        all_stores = response.json()
        # Filter stores that have coordinates
        stores_with_coords = [s for s in all_stores if s.get('lat') and s.get('lon')]
        
        if not stores_with_coords:
            return [TextContent(type='text', text='No stores have location coordinates available.')]
        
        # Calculate distances (simple haversine approximation)
        import math
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            R = 6371  # Earth's radius in km
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = (math.sin(dlat/2) * math.sin(dlat/2) +
                 math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                 math.sin(dlon/2) * math.sin(dlon/2))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c
        
        nearby_stores = []
        for store in stores_with_coords:
            distance = calculate_distance(lat, lon, store['lat'], store['lon'])
            if distance <= radius_km:
                store['distance'] = distance
                nearby_stores.append(store)
        
        # Sort by distance
        nearby_stores.sort(key=lambda x: x['distance'])
        
        if not nearby_stores:
            return [TextContent(type='text', text=f'No stores found within {radius_km}km of the specified location.')]
        
        result = f'Found {len(nearby_stores)} stores within {radius_km}km:\\n\\n'
        for store in nearby_stores:
            result += f'**{store["name"]}** ({store["type"]})\\n'
            result += f'Distance: {store["distance"]:.1f}km\\n'
            if store.get('address'):
                result += f'Address: {store["address"]}\\n'
            result += f'ID: {store["id"]}\\n\\n'
        
        return [TextContent(type='text', text=result)]


if __name__ == '__main__':
    # This will be called by the run script
    logger.info('Starting Partle Stores MCP Server')
    mcp_server.run()
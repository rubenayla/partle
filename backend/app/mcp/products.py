"""MCP Server for Partle Products API integration."""
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
mcp_server = Server('partle-products')


@contextmanager
def get_http_client():
    """Get HTTP client for API requests."""
    with httpx.Client(base_url=API_BASE_URL) as client:
        yield client


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for products management."""
    return [
        Tool(
            name='search_products',
            description='Search and filter products by various criteria including name, price range, store, and tags',
            inputSchema={
                'type': 'object',
                'properties': {
                    'q': {
                        'type': 'string', 
                        'description': 'Search query for product name or description'
                    },
                    'store_id': {
                        'type': 'integer',
                        'description': 'Filter by specific store ID'
                    },
                    'store_name': {
                        'type': 'string',
                        'description': 'Filter by store name (partial match)'
                    },
                    'min_price': {
                        'type': 'number',
                        'description': 'Minimum price filter'
                    },
                    'max_price': {
                        'type': 'number', 
                        'description': 'Maximum price filter'
                    },
                    'tags': {
                        'type': 'string',
                        'description': 'Comma-separated list of tags to filter by'
                    },
                    'sort_by': {
                        'type': 'string',
                        'enum': ['price_desc', 'name_asc', 'random'],
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
            name='get_product',
            description='Get detailed information about a specific product by ID',
            inputSchema={
                'type': 'object',
                'properties': {
                    'product_id': {
                        'type': 'integer',
                        'description': 'The ID of the product to retrieve'
                    }
                },
                'required': ['product_id']
            }
        ),
        Tool(
            name='get_products_by_store',
            description='Get all products from a specific store',
            inputSchema={
                'type': 'object',
                'properties': {
                    'store_id': {
                        'type': 'integer',
                        'description': 'The ID of the store'
                    }
                },
                'required': ['store_id']
            }
        ),
        Tool(
            name='search_products_elasticsearch',
            description='Advanced product search using Elasticsearch with complex filtering and faceted search',
            inputSchema={
                'type': 'object',
                'properties': {
                    'q': {
                        'type': 'string',
                        'description': 'Search query'
                    },
                    'stores': {
                        'type': 'string',
                        'description': 'Comma-separated store IDs to filter by'
                    },
                    'min_price': {
                        'type': 'number',
                        'description': 'Minimum price'
                    },
                    'max_price': {
                        'type': 'number',
                        'description': 'Maximum price'
                    },
                    'tags': {
                        'type': 'string',
                        'description': 'Comma-separated tags'
                    },
                    'include_test_data': {
                        'type': 'boolean',
                        'default': False,
                        'description': 'Include mock/test data in results (default: False)'
                    },
                    'location': {
                        'type': 'string',
                        'description': 'Location in format "lat,lon,radius_km"'
                    },
                    'size': {
                        'type': 'integer',
                        'default': 20,
                        'description': 'Number of results'
                    },
                    'from_': {
                        'type': 'integer',
                        'default': 0,
                        'description': 'Offset for pagination'
                    }
                }
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[TextContent]:
    """Handle tool calls for products operations."""
    try:
        if name == 'search_products':
            return await _search_products(arguments or {})
        elif name == 'get_product':
            return await _get_product(arguments or {})
        elif name == 'get_products_by_store':
            return await _get_products_by_store(arguments or {})
        elif name == 'search_products_elasticsearch':
            return await _search_products_elasticsearch(arguments or {})
        else:
            return [TextContent(type='text', text=f'Unknown tool: {name}')]
    except Exception as e:
        logger.error(f'Error calling tool {name}: {e}')
        return [TextContent(type='text', text=f'Error: {str(e)}')]


async def _search_products(args: Dict[str, Any]) -> List[TextContent]:
    """Search products with various filters."""
    with get_http_client() as client:
        params = {k: v for k, v in args.items() if v is not None}
        response = client.get('/v1/products/', params=params)
        response.raise_for_status()
        
        products = response.json()
        if not products:
            return [TextContent(type='text', text='No products found matching your criteria.')]
        
        result = f'Found {len(products)} products:\\n\\n'
        for product in products:
            result += f'**{product["name"]}**\\n'
            if product.get('price'):
                result += f'Price: €{product["price"]}\\n'
            if product.get('description'):
                result += f'Description: {product["description"]}\\n'
            if product.get('store'):
                result += f'Store: {product["store"]["name"]}\\n'
            if product.get('tags'):
                tags = [tag['name'] for tag in product['tags']]
                result += f'Tags: {", ".join(tags)}\\n'
            result += f'ID: {product["id"]}\\n\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_product(args: Dict[str, Any]) -> List[TextContent]:
    """Get specific product details."""
    product_id = args.get('product_id')
    if not product_id:
        return [TextContent(type='text', text='Error: product_id is required')]
    
    with get_http_client() as client:
        response = client.get(f'/v1/products/{product_id}')
        if response.status_code == 404:
            return [TextContent(type='text', text=f'Product with ID {product_id} not found.')]
        
        response.raise_for_status()
        product = response.json()
        
        result = f'**{product["name"]}**\\n\\n'
        if product.get('price'):
            result += f'**Price:** €{product["price"]}\\n'
        if product.get('spec'):
            result += f'**Specification:** {product["spec"]}\\n'
        if product.get('description'):
            result += f'**Description:** {product["description"]}\\n'
        if product.get('url'):
            result += f'**URL:** {product["url"]}\\n'
        if product.get('store'):
            result += f'**Store:** {product["store"]["name"]}\\n'
            if product["store"].get('address'):
                result += f'**Store Address:** {product["store"]["address"]}\\n'
        if product.get('tags'):
            tags = [tag['name'] for tag in product['tags']]
            result += f'**Tags:** {", ".join(tags)}\\n'
        
        result += f'\\n**Product ID:** {product["id"]}\\n'
        if product.get('created_at'):
            result += f'**Created:** {product["created_at"]}\\n'
        if product.get('updated_at'):
            result += f'**Last Updated:** {product["updated_at"]}\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_products_by_store(args: Dict[str, Any]) -> List[TextContent]:
    """Get all products from a specific store."""
    store_id = args.get('store_id')
    if not store_id:
        return [TextContent(type='text', text='Error: store_id is required')]

    # Build params with include_test_data if provided
    params = {}
    if 'include_test_data' in args:
        params['include_test_data'] = args['include_test_data']

    with get_http_client() as client:
        response = client.get(f'/v1/products/store/{store_id}', params=params)
        if response.status_code == 404:
            return [TextContent(type='text', text=f'Store with ID {store_id} not found or has no products.')]
        
        response.raise_for_status()
        products = response.json()
        
        if not products:
            return [TextContent(type='text', text=f'No products found for store ID {store_id}.')]
        
        result = f'Found {len(products)} products in store:\\n\\n'
        for product in products:
            result += f'• **{product["name"]}**'
            if product.get('price'):
                result += f' - €{product["price"]}'
            result += f' (ID: {product["id"]})\\n'
        
        return [TextContent(type='text', text=result)]


async def _search_products_elasticsearch(args: Dict[str, Any]) -> List[TextContent]:
    """Advanced product search using Elasticsearch."""
    with get_http_client() as client:
        params = {k: v for k, v in args.items() if v is not None}
        # Handle the 'from_' parameter (rename to 'from' for API)
        if 'from_' in params:
            params['from'] = params.pop('from_')
        
        response = client.get('/v1/search/products/', params=params)
        if response.status_code == 503:
            return [TextContent(type='text', text='Elasticsearch search is currently unavailable. Try using the basic search_products tool instead.')]
        
        response.raise_for_status()
        search_results = response.json()
        
        products = search_results.get('products', [])
        total = search_results.get('total', 0)
        
        if not products:
            return [TextContent(type='text', text='No products found matching your search criteria.')]
        
        result = f'Found {total} total products (showing {len(products)}):\\n\\n'
        
        for product in products:
            result += f'**{product["name"]}**\\n'
            if product.get('price'):
                result += f'Price: €{product["price"]}\\n'
            if product.get('description'):
                result += f'Description: {product["description"]}\\n'
            if product.get('store'):
                result += f'Store: {product["store"]["name"]}\\n'
            if product.get('tags'):
                tags = [tag['name'] for tag in product['tags']]
                result += f'Tags: {", ".join(tags)}\\n'
            if product.get('_score'):
                result += f'Relevance Score: {product["_score"]:.2f}\\n'
            result += f'ID: {product["id"]}\\n\\n'
        
        # Add aggregations info if available
        if 'aggregations' in search_results:
            aggs = search_results['aggregations']
            result += '\\n**Search Facets:**\\n'
            
            if 'stores' in aggs:
                result += '**Stores:**\\n'
                for bucket in aggs['stores']['buckets']:
                    result += f'  • {bucket["key"]}: {bucket["doc_count"]} products\\n'
            
            if 'tags' in aggs:
                result += '**Tags:**\\n'
                for bucket in aggs['tags']['buckets']:
                    result += f'  • {bucket["key"]}: {bucket["doc_count"]} products\\n'
            
            if 'price_stats' in aggs:
                stats = aggs['price_stats']
                result += f'**Price Range:** €{stats["min"]:.2f} - €{stats["max"]:.2f}\\n'
                result += f'**Average Price:** €{stats["avg"]:.2f}\\n'
        
        return [TextContent(type='text', text=result)]


if __name__ == '__main__':
    # This will be called by the run script
    logger.info('Starting Partle Products MCP Server')
    mcp_server.run()
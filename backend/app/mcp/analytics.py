"""MCP Server for Partle Analytics and Business Intelligence."""
import logging
from typing import Optional, Any, Dict, List
from contextlib import contextmanager
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import json
import os
from collections import Counter
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
API_BASE_URL = os.getenv('PARTLE_API_URL', 'http://localhost:8000')

# Initialize MCP server
mcp_server = Server('partle-analytics')


@contextmanager
def get_http_client():
    """Get HTTP client for API requests."""
    with httpx.Client(base_url=API_BASE_URL) as client:
        yield client


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for analytics and business intelligence."""
    return [
        Tool(
            name='get_platform_overview',
            description='Get a comprehensive overview of the entire Partle platform including total counts, recent activity, and key metrics',
            inputSchema={
                'type': 'object',
                'properties': {}
            }
        ),
        Tool(
            name='analyze_products',
            description='Analyze products across the platform with detailed statistics and insights',
            inputSchema={
                'type': 'object',
                'properties': {
                    'include_price_analysis': {
                        'type': 'boolean',
                        'default': True,
                        'description': 'Include price statistics and analysis'
                    },
                    'include_tag_analysis': {
                        'type': 'boolean',
                        'default': True,
                        'description': 'Include tag distribution analysis'
                    },
                    'include_store_breakdown': {
                        'type': 'boolean',
                        'default': True,
                        'description': 'Include per-store product breakdown'
                    }
                }
            }
        ),
        Tool(
            name='analyze_stores',
            description='Analyze stores across the platform with distribution and performance metrics',
            inputSchema={
                'type': 'object',
                'properties': {
                    'include_location_analysis': {
                        'type': 'boolean',
                        'default': True,
                        'description': 'Analyze geographic distribution of stores'
                    },
                    'include_product_counts': {
                        'type': 'boolean',
                        'default': True,
                        'description': 'Include product counts per store'
                    }
                }
            }
        ),
        Tool(
            name='get_top_performers',
            description='Get top performing entities (stores with most products, most expensive products, etc.)',
            inputSchema={
                'type': 'object',
                'properties': {
                    'metric': {
                        'type': 'string',
                        'enum': ['stores_by_products', 'products_by_price', 'popular_tags'],
                        'default': 'stores_by_products',
                        'description': 'Metric to rank by'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 10,
                        'description': 'Number of top results to return'
                    }
                }
            }
        ),
        Tool(
            name='analyze_tags',
            description='Comprehensive analysis of tags usage across products and stores',
            inputSchema={
                'type': 'object',
                'properties': {
                    'min_usage_count': {
                        'type': 'integer',
                        'default': 1,
                        'description': 'Minimum usage count to include tag in analysis'
                    }
                }
            }
        ),
        Tool(
            name='get_market_insights',
            description='Generate market insights including price ranges, competitive analysis, and market gaps',
            inputSchema={
                'type': 'object',
                'properties': {
                    'category_tag': {
                        'type': 'string',
                        'description': 'Focus analysis on products with specific tag/category'
                    }
                }
            }
        ),
        Tool(
            name='compare_stores',
            description='Compare multiple stores across various metrics',
            inputSchema={
                'type': 'object',
                'properties': {
                    'store_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'List of store IDs to compare'
                    }
                },
                'required': ['store_ids']
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[TextContent]:
    """Handle tool calls for analytics operations."""
    try:
        if name == 'get_platform_overview':
            return await _get_platform_overview(arguments or {})
        elif name == 'analyze_products':
            return await _analyze_products(arguments or {})
        elif name == 'analyze_stores':
            return await _analyze_stores(arguments or {})
        elif name == 'get_top_performers':
            return await _get_top_performers(arguments or {})
        elif name == 'analyze_tags':
            return await _analyze_tags(arguments or {})
        elif name == 'get_market_insights':
            return await _get_market_insights(arguments or {})
        elif name == 'compare_stores':
            return await _compare_stores(arguments or {})
        else:
            return [TextContent(type='text', text=f'Unknown tool: {name}')]
    except Exception as e:
        logger.error(f'Error calling tool {name}: {e}')
        return [TextContent(type='text', text=f'Error: {str(e)}')]


async def _get_platform_overview(args: Dict[str, Any]) -> List[TextContent]:
    """Get comprehensive platform overview."""
    with get_http_client() as client:
        # Fetch all stores and products
        stores_response = client.get('/v1/stores/')
        products_response = client.get('/v1/products/', params={'limit': 1000})  # Get more products
        
        stores_response.raise_for_status()
        products_response.raise_for_status()
        
        stores = stores_response.json()
        products = products_response.json()
        
        result = '# 📊 Partle Platform Overview\\n\\n'
        
        # Basic counts
        result += f'**Total Stores:** {len(stores)}\\n'
        result += f'**Total Products:** {len(products)}\\n\\n'
        
        # Store type breakdown
        if stores:
            store_types = Counter(s.get('type', 'unknown') for s in stores)
            result += '**Store Types:**\\n'
            for store_type, count in store_types.items():
                result += f'  • {store_type.title()}: {count}\\n'
            result += '\\n'
        
        # Product statistics
        if products:
            products_with_prices = [p for p in products if p.get('price') is not None]
            result += f'**Products with Prices:** {len(products_with_prices)} of {len(products)}\\n'
            
            if products_with_prices:
                prices = [p['price'] for p in products_with_prices]
                result += f'**Price Range:** €{min(prices):.2f} - €{max(prices):.2f}\\n'
                result += f'**Average Price:** €{sum(prices)/len(prices):.2f}\\n'
            
            # Store distribution
            store_product_counts = Counter(p.get('store_id') for p in products if p.get('store_id'))
            result += f'\\n**Products Distribution:**\\n'
            result += f'  • Orphan Products (no store): {len(products) - sum(store_product_counts.values())}\\n'
            result += f'  • Stores with Products: {len(store_product_counts)}\\n'
            if store_product_counts:
                avg_products_per_store = sum(store_product_counts.values()) / len(store_product_counts)
                result += f'  • Avg Products per Store: {avg_products_per_store:.1f}\\n'
        
        # Tag analysis
        all_tags = []
        for product in products:
            if product.get('tags'):
                all_tags.extend([tag['name'] for tag in product['tags']])
        for store in stores:
            if store.get('tags'):
                all_tags.extend([tag['name'] for tag in store['tags']])
        
        if all_tags:
            unique_tags = len(set(all_tags))
            result += f'\\n**Tags:**\\n'
            result += f'  • Unique Tags: {unique_tags}\\n'
            result += f'  • Total Tag Usage: {len(all_tags)}\\n'
            
            most_common = Counter(all_tags).most_common(5)
            result += f'  • Top Tags: {", ".join([f"{tag} ({count})" for tag, count in most_common])}\\n'
        
        return [TextContent(type='text', text=result)]


async def _analyze_products(args: Dict[str, Any]) -> List[TextContent]:
    """Analyze products with detailed statistics."""
    include_price = args.get('include_price_analysis', True)
    include_tags = args.get('include_tag_analysis', True)
    include_stores = args.get('include_store_breakdown', True)
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        if not products:
            return [TextContent(type='text', text='No products found for analysis.')]
        
        result = '# 🛍️ Product Analysis\\n\\n'
        result += f'**Total Products Analyzed:** {len(products)}\\n\\n'
        
        # Price analysis
        if include_price:
            products_with_prices = [p for p in products if p.get('price') is not None]
            result += '## 💰 Price Analysis\\n'
            result += f'**Products with Prices:** {len(products_with_prices)} ({len(products_with_prices)/len(products)*100:.1f}%)\\n'
            
            if products_with_prices:
                prices = [float(p['price']) for p in products_with_prices]
                prices.sort()
                
                result += f'**Price Range:** €{min(prices):.2f} - €{max(prices):.2f}\\n'
                result += f'**Average Price:** €{sum(prices)/len(prices):.2f}\\n'
                result += f'**Median Price:** €{prices[len(prices)//2]:.2f}\\n'
                
                # Price distribution
                ranges = [
                    (0, 10, '€0-10'),
                    (10, 50, '€10-50'),
                    (50, 100, '€50-100'),
                    (100, 500, '€100-500'),
                    (500, float('inf'), '€500+')
                ]
                
                result += '\\n**Price Distribution:**\\n'
                for min_price, max_price, label in ranges:
                    count = sum(1 for p in prices if min_price <= p < max_price)
                    if count > 0:
                        result += f'  • {label}: {count} products ({count/len(prices)*100:.1f}%)\\n'
            
            result += '\\n'
        
        # Tag analysis
        if include_tags:
            all_product_tags = []
            for product in products:
                if product.get('tags'):
                    all_product_tags.extend([tag['name'] for tag in product['tags']])
            
            result += '## 🏷️ Tag Analysis\\n'
            if all_product_tags:
                tag_counts = Counter(all_product_tags)
                result += f'**Unique Tags:** {len(set(all_product_tags))}\\n'
                result += f'**Tagged Products:** {len([p for p in products if p.get("tags")])}\\n'
                result += f'**Avg Tags per Tagged Product:** {len(all_product_tags) / len([p for p in products if p.get("tags")]):.1f}\\n'
                
                result += '\\n**Top Product Tags:**\\n'
                for tag, count in tag_counts.most_common(10):
                    result += f'  • {tag}: {count} products\\n'
            else:
                result += 'No tags found on products.\\n'
            result += '\\n'
        
        # Store breakdown
        if include_stores:
            store_product_counts = Counter(p.get('store_id') for p in products if p.get('store_id'))
            orphan_count = len(products) - sum(store_product_counts.values())
            
            result += '## 🏪 Store Breakdown\\n'
            result += f'**Orphan Products:** {orphan_count}\\n'
            result += f'**Stores with Products:** {len(store_product_counts)}\\n'
            
            if store_product_counts:
                result += '\\n**Top Stores by Product Count:**\\n'
                # Get store names for the top stores
                stores_response = client.get('/v1/stores/')
                stores_response.raise_for_status()
                stores = {s['id']: s['name'] for s in stores_response.json()}
                
                for store_id, count in store_product_counts.most_common(10):
                    store_name = stores.get(store_id, f'Store {store_id}')
                    result += f'  • {store_name}: {count} products\\n'
        
        return [TextContent(type='text', text=result)]


async def _analyze_stores(args: Dict[str, Any]) -> List[TextContent]:
    """Analyze stores with distribution and performance metrics."""
    include_location = args.get('include_location_analysis', True)
    include_products = args.get('include_product_counts', True)
    
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        stores_response.raise_for_status()
        stores = stores_response.json()
        
        if not stores:
            return [TextContent(type='text', text='No stores found for analysis.')]
        
        result = '# 🏪 Store Analysis\\n\\n'
        result += f'**Total Stores Analyzed:** {len(stores)}\\n\\n'
        
        # Type distribution
        store_types = Counter(s.get('type', 'unknown') for s in stores)
        result += '## 📊 Store Type Distribution\\n'
        for store_type, count in store_types.items():
            percentage = count / len(stores) * 100
            result += f'  • **{store_type.title()}:** {count} stores ({percentage:.1f}%)\\n'
        result += '\\n'
        
        # Location analysis
        if include_location:
            stores_with_coords = [s for s in stores if s.get('lat') and s.get('lon')]
            stores_with_addresses = [s for s in stores if s.get('address')]
            
            result += '## 📍 Location Analysis\\n'
            result += f'**Stores with Coordinates:** {len(stores_with_coords)} ({len(stores_with_coords)/len(stores)*100:.1f}%)\\n'
            result += f'**Stores with Addresses:** {len(stores_with_addresses)} ({len(stores_with_addresses)/len(stores)*100:.1f}%)\\n'
            
            if stores_with_coords:
                # Basic geographic analysis
                lats = [s['lat'] for s in stores_with_coords]
                lons = [s['lon'] for s in stores_with_coords]
                result += f'**Geographic Range:**\\n'
                result += f'  • Latitude: {min(lats):.3f} to {max(lats):.3f}\\n'
                result += f'  • Longitude: {min(lons):.3f} to {max(lons):.3f}\\n'
            result += '\\n'
        
        # Product count analysis
        if include_products:
            products_response = client.get('/v1/products/', params={'limit': 1000})
            products_response.raise_for_status()
            products = products_response.json()
            
            store_product_counts = Counter(p.get('store_id') for p in products if p.get('store_id'))
            
            result += '## 📦 Product Distribution\\n'
            stores_with_products = len(store_product_counts)
            stores_without_products = len(stores) - stores_with_products
            
            result += f'**Stores with Products:** {stores_with_products}\\n'
            result += f'**Empty Stores:** {stores_without_products}\\n'
            
            if store_product_counts:
                product_counts = list(store_product_counts.values())
                result += f'**Avg Products per Store:** {sum(product_counts) / len(product_counts):.1f}\\n'
                result += f'**Most Products in Store:** {max(product_counts)}\\n'
                result += f'**Least Products in Store:** {min(product_counts)}\\n'
                
                # Distribution ranges
                ranges = [
                    (1, 5, '1-5 products'),
                    (6, 20, '6-20 products'),
                    (21, 50, '21-50 products'),
                    (51, float('inf'), '50+ products')
                ]
                
                result += '\\n**Store Size Distribution:**\\n'
                for min_count, max_count, label in ranges:
                    count = sum(1 for c in product_counts if min_count <= c < max_count)
                    if count > 0:
                        result += f'  • {label}: {count} stores\\n'
        
        # Website/homepage analysis
        stores_with_websites = [s for s in stores if s.get('homepage')]
        result += f'\\n## 🌐 Digital Presence\\n'
        result += f'**Stores with Websites:** {len(stores_with_websites)} ({len(stores_with_websites)/len(stores)*100:.1f}%)\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_top_performers(args: Dict[str, Any]) -> List[TextContent]:
    """Get top performing entities by various metrics."""
    metric = args.get('metric', 'stores_by_products')
    limit = args.get('limit', 10)
    
    with get_http_client() as client:
        if metric == 'stores_by_products':
            # Get stores with most products
            stores_response = client.get('/v1/stores/')
            products_response = client.get('/v1/products/', params={'limit': 1000})
            
            stores_response.raise_for_status()
            products_response.raise_for_status()
            
            stores = {s['id']: s for s in stores_response.json()}
            products = products_response.json()
            
            store_counts = Counter(p.get('store_id') for p in products if p.get('store_id'))
            
            result = f'# 🏆 Top {limit} Stores by Product Count\\n\\n'
            for i, (store_id, count) in enumerate(store_counts.most_common(limit), 1):
                store = stores.get(store_id, {})
                store_name = store.get('name', f'Store {store_id}')
                store_type = store.get('type', 'unknown')
                result += f'{i}. **{store_name}** ({store_type}) - {count} products\\n'
            
        elif metric == 'products_by_price':
            # Get most expensive products
            products_response = client.get('/v1/products/', params={'limit': 1000, 'sort_by': 'price_desc'})
            products_response.raise_for_status()
            products = products_response.json()
            
            expensive_products = [p for p in products if p.get('price') is not None]
            expensive_products.sort(key=lambda x: float(x['price']), reverse=True)
            
            result = f'# 💰 Top {limit} Most Expensive Products\\n\\n'
            for i, product in enumerate(expensive_products[:limit], 1):
                store_name = product.get('store', {}).get('name', 'Unknown Store') if product.get('store') else 'No Store'
                result += f'{i}. **{product["name"]}** - €{product["price"]} ({store_name})\\n'
            
        elif metric == 'popular_tags':
            # Get most popular tags
            products_response = client.get('/v1/products/', params={'limit': 1000})
            stores_response = client.get('/v1/stores/')
            
            products_response.raise_for_status()
            stores_response.raise_for_status()
            
            products = products_response.json()
            stores = stores_response.json()
            
            all_tags = []
            for product in products:
                if product.get('tags'):
                    all_tags.extend([tag['name'] for tag in product['tags']])
            for store in stores:
                if store.get('tags'):
                    all_tags.extend([tag['name'] for tag in store['tags']])
            
            tag_counts = Counter(all_tags)
            
            result = f'# 🏷️ Top {limit} Most Popular Tags\\n\\n'
            for i, (tag, count) in enumerate(tag_counts.most_common(limit), 1):
                result += f'{i}. **{tag}** - {count} uses\\n'
        
        return [TextContent(type='text', text=result)]


async def _analyze_tags(args: Dict[str, Any]) -> List[TextContent]:
    """Comprehensive analysis of tags usage."""
    min_usage = args.get('min_usage_count', 1)
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        stores_response = client.get('/v1/stores/')
        
        products_response.raise_for_status()
        stores_response.raise_for_status()
        
        products = products_response.json()
        stores = stores_response.json()
        
        # Collect tags
        product_tags = []
        store_tags = []
        
        for product in products:
            if product.get('tags'):
                product_tags.extend([tag['name'] for tag in product['tags']])
        
        for store in stores:
            if store.get('tags'):
                store_tags.extend([tag['name'] for tag in store['tags']])
        
        all_tags = product_tags + store_tags
        
        if not all_tags:
            return [TextContent(type='text', text='No tags found in the system.')]
        
        tag_counts = Counter(all_tags)
        product_tag_counts = Counter(product_tags)
        store_tag_counts = Counter(store_tags)
        
        # Filter by minimum usage
        filtered_tags = {tag: count for tag, count in tag_counts.items() if count >= min_usage}
        
        result = '# 🏷️ Tag Analysis\\n\\n'
        result += f'**Total Unique Tags:** {len(set(all_tags))}\\n'
        result += f'**Tags Meeting Criteria (≥{min_usage} uses):** {len(filtered_tags)}\\n'
        result += f'**Total Tag Usage:** {len(all_tags)}\\n\\n'
        
        result += '## Usage Breakdown\\n'
        result += f'**Product Tags:** {len(product_tags)} uses across {len(set(product_tags))} unique tags\\n'
        result += f'**Store Tags:** {len(store_tags)} uses across {len(set(store_tags))} unique tags\\n\\n'
        
        # Tag categories (basic classification)
        result += '## Top Tags by Category\\n\\n'
        
        result += '**Most Used Tags Overall:**\\n'
        for tag, count in Counter(filtered_tags).most_common(15):
            product_uses = product_tag_counts.get(tag, 0)
            store_uses = store_tag_counts.get(tag, 0)
            result += f'  • **{tag}**: {count} total ({product_uses} products, {store_uses} stores)\\n'
        
        # Exclusive tags
        product_only_tags = set(product_tags) - set(store_tags)
        store_only_tags = set(store_tags) - set(product_tags)
        shared_tags = set(product_tags) & set(store_tags)
        
        result += f'\\n**Tag Distribution:**\\n'
        result += f'  • Product-only tags: {len(product_only_tags)}\\n'
        result += f'  • Store-only tags: {len(store_only_tags)}\\n'
        result += f'  • Shared tags: {len(shared_tags)}\\n'
        
        if shared_tags:
            result += f'\\n**Most Popular Shared Tags:**\\n'
            shared_tag_counts = {tag: tag_counts[tag] for tag in shared_tags}
            for tag, count in Counter(shared_tag_counts).most_common(5):
                result += f'  • {tag}: {count} uses\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_market_insights(args: Dict[str, Any]) -> List[TextContent]:
    """Generate market insights and competitive analysis."""
    category_tag = args.get('category_tag')
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        stores_response = client.get('/v1/stores/')
        
        products_response.raise_for_status()
        stores_response.raise_for_status()
        
        products = products_response.json()
        stores = stores_response.json()
        
        # Filter by category if specified
        if category_tag:
            products = [p for p in products if p.get('tags') and 
                       any(tag['name'].lower() == category_tag.lower() for tag in p['tags'])]
            if not products:
                return [TextContent(type='text', text=f'No products found with tag "{category_tag}".')]
        
        result = f'# 📈 Market Insights{f" - {category_tag}" if category_tag else ""}\\n\\n'
        
        # Market size and composition
        result += '## Market Overview\\n'
        result += f'**Total Products in Analysis:** {len(products)}\\n'
        
        products_with_prices = [p for p in products if p.get('price') is not None]
        if products_with_prices:
            prices = [float(p['price']) for p in products_with_prices]
            result += f'**Products with Pricing:** {len(products_with_prices)} ({len(products_with_prices)/len(products)*100:.1f}%)\\n'
            result += f'**Market Value Range:** €{min(prices):.2f} - €{max(prices):.2f}\\n'
            result += f'**Average Market Price:** €{sum(prices)/len(prices):.2f}\\n\\n'
            
            # Price segments
            segments = [
                (0, 20, 'Budget'),
                (20, 100, 'Mid-range'),
                (100, 500, 'Premium'),
                (500, float('inf'), 'Luxury')
            ]
            
            result += '## Price Segments\\n'
            for min_price, max_price, segment in segments:
                count = sum(1 for p in prices if min_price <= p < max_price)
                if count > 0:
                    avg_price = sum(p for p in prices if min_price <= p < max_price) / count
                    result += f'**{segment} (€{min_price}-{max_price if max_price != float("inf") else "∞"}):** {count} products, avg €{avg_price:.2f}\\n'
            result += '\\n'
        
        # Competitive landscape
        store_product_counts = Counter(p.get('store_id') for p in products if p.get('store_id'))
        stores_dict = {s['id']: s for s in stores}
        
        result += '## Competitive Landscape\\n'
        result += f'**Active Stores in Market:** {len(store_product_counts)}\\n'
        
        if store_product_counts:
            top_competitors = store_product_counts.most_common(5)
            result += '\\n**Market Leaders:**\\n'
            total_market_products = sum(store_product_counts.values())
            
            for i, (store_id, count) in enumerate(top_competitors, 1):
                store = stores_dict.get(store_id, {})
                store_name = store.get('name', f'Store {store_id}')
                market_share = count / total_market_products * 100
                result += f'{i}. **{store_name}**: {count} products ({market_share:.1f}% market share)\\n'
            
            # Market concentration
            top_3_share = sum(count for _, count in top_competitors[:3]) / total_market_products * 100
            result += f'\\n**Market Concentration:** Top 3 stores control {top_3_share:.1f}% of products\\n'
        
        # Category analysis
        if not category_tag:
            all_tags = []
            for product in products:
                if product.get('tags'):
                    all_tags.extend([tag['name'] for tag in product['tags']])
            
            if all_tags:
                category_counts = Counter(all_tags)
                result += '\\n## Product Categories\\n'
                result += '**Most Popular Categories:**\\n'
                for category, count in category_counts.most_common(10):
                    percentage = count / len(products) * 100
                    result += f'  • {category}: {count} products ({percentage:.1f}%)\\n'
        
        # Market opportunities
        result += '\\n## Market Opportunities\\n'
        
        # Stores without products in this category
        all_store_ids = {s['id'] for s in stores}
        active_store_ids = set(store_product_counts.keys())
        inactive_stores = all_store_ids - active_store_ids
        
        if inactive_stores:
            result += f'**Potential Market Expansion:** {len(inactive_stores)} stores have no products in this category\\n'
        
        # Price gaps
        if products_with_prices and len(products_with_prices) > 1:
            sorted_prices = sorted(set(prices))
            gaps = []
            for i in range(len(sorted_prices) - 1):
                gap = sorted_prices[i + 1] - sorted_prices[i]
                if gap > 50:  # Significant price gap
                    gaps.append((sorted_prices[i], sorted_prices[i + 1], gap))
            
            if gaps:
                result += '**Price Gaps (Potential Opportunities):**\\n'
                for low, high, gap in gaps[:3]:
                    result += f'  • €{low:.2f} to €{high:.2f} (gap: €{gap:.2f})\\n'
        
        return [TextContent(type='text', text=result)]


async def _compare_stores(args: Dict[str, Any]) -> List[TextContent]:
    """Compare multiple stores across various metrics."""
    store_ids = args.get('store_ids', [])
    
    if not store_ids:
        return [TextContent(type='text', text='Error: store_ids list is required')]
    
    if len(store_ids) < 2:
        return [TextContent(type='text', text='Error: At least 2 store IDs are required for comparison')]
    
    with get_http_client() as client:
        # Get store details
        stores = []
        for store_id in store_ids:
            try:
                store_response = client.get(f'/v1/stores/{store_id}')
                store_response.raise_for_status()
                stores.append(store_response.json())
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return [TextContent(type='text', text=f'Store with ID {store_id} not found')]
                raise
        
        # Get products for comparison
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        all_products = products_response.json()
        
        result = f'# 🔄 Store Comparison ({len(stores)} stores)\\n\\n'
        
        # Store overview table
        result += '## Basic Information\\n'
        result += '| Store | Type | Location | Website |\\n'
        result += '|-------|------|----------|---------|\\n'
        
        for store in stores:
            location = store.get('address', 'No address')
            if store.get('lat') and store.get('lon'):
                location += f' ({store["lat"]:.3f}, {store["lon"]:.3f})'
            website = store.get('homepage', 'No website')
            result += f'| {store["name"]} | {store["type"]} | {location} | {website} |\\n'
        
        result += '\\n## Product Portfolio Analysis\\n'
        
        # Product counts and statistics for each store
        for store in stores:
            store_products = [p for p in all_products if p.get('store_id') == store['id']]
            
            result += f'\\n### {store["name"]}\\n'
            result += f'**Product Count:** {len(store_products)}\\n'
            
            if store_products:
                products_with_prices = [p for p in store_products if p.get('price') is not None]
                if products_with_prices:
                    prices = [float(p['price']) for p in products_with_prices]
                    result += f'**Price Range:** €{min(prices):.2f} - €{max(prices):.2f}\\n'
                    result += f'**Average Price:** €{sum(prices)/len(prices):.2f}\\n'
                    result += f'**Pricing Coverage:** {len(products_with_prices)} of {len(store_products)} products ({len(products_with_prices)/len(store_products)*100:.1f}%)\\n'
                
                # Tag analysis
                store_tags = []
                for product in store_products:
                    if product.get('tags'):
                        store_tags.extend([tag['name'] for tag in product['tags']])
                
                if store_tags:
                    unique_tags = len(set(store_tags))
                    result += f'**Categories/Tags:** {unique_tags} unique categories\\n'
                    top_tags = Counter(store_tags).most_common(3)
                    result += f'**Top Categories:** {", ".join([f"{tag} ({count})" for tag, count in top_tags])}\\n'
            else:
                result += 'No products in this store.\\n'
        
        # Comparative metrics
        result += '\\n## Comparative Metrics\\n'
        
        store_metrics = []
        for store in stores:
            store_products = [p for p in all_products if p.get('store_id') == store['id']]
            products_with_prices = [p for p in store_products if p.get('price') is not None]
            
            metrics = {
                'name': store['name'],
                'product_count': len(store_products),
                'avg_price': sum(float(p['price']) for p in products_with_prices) / len(products_with_prices) if products_with_prices else 0,
                'price_coverage': len(products_with_prices) / len(store_products) * 100 if store_products else 0,
                'has_location': bool(store.get('lat') and store.get('lon')),
                'has_website': bool(store.get('homepage'))
            }
            store_metrics.append(metrics)
        
        # Rankings
        result += '**Rankings:**\\n'
        
        # By product count
        by_products = sorted(store_metrics, key=lambda x: x['product_count'], reverse=True)
        result += f'  • Most Products: {by_products[0]["name"]} ({by_products[0]["product_count"]} products)\\n'
        
        # By average price
        by_price = [s for s in store_metrics if s['avg_price'] > 0]
        if by_price:
            by_price.sort(key=lambda x: x['avg_price'], reverse=True)
            result += f'  • Highest Avg Price: {by_price[0]["name"]} (€{by_price[0]["avg_price"]:.2f})\\n'
            result += f'  • Lowest Avg Price: {by_price[-1]["name"]} (€{by_price[-1]["avg_price"]:.2f})\\n'
        
        # Digital presence
        digital_stores = [s for s in store_metrics if s['has_website']]
        located_stores = [s for s in store_metrics if s['has_location']]
        
        result += f'\\n**Digital Presence:**\\n'
        result += f'  • Stores with Websites: {len(digital_stores)} of {len(stores)}\\n'
        result += f'  • Stores with Location Data: {len(located_stores)} of {len(stores)}\\n'
        
        return [TextContent(type='text', text=result)]


if __name__ == '__main__':
    # This will be called by the run script
    logger.info('Starting Partle Analytics MCP Server')
    mcp_server.run()
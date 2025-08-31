"""MCP Server for Partle Price Intelligence and Market Analysis."""
import logging
from typing import Optional, Any, Dict, List
from contextlib import contextmanager
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import json
import os
from collections import defaultdict, Counter
from statistics import median, mean
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
API_BASE_URL = os.getenv('PARTLE_API_URL', 'http://localhost:8000')

# Initialize MCP server
mcp_server = Server('partle-price-intelligence')


@contextmanager
def get_http_client():
    """Get HTTP client for API requests."""
    with httpx.Client(base_url=API_BASE_URL) as client:
        yield client


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for price intelligence."""
    return [
        Tool(
            name='analyze_price_trends',
            description='Analyze price trends and patterns across products and categories',
            inputSchema={
                'type': 'object',
                'properties': {
                    'category_tag': {
                        'type': 'string',
                        'description': 'Focus analysis on specific category/tag'
                    },
                    'store_id': {
                        'type': 'integer',
                        'description': 'Focus analysis on specific store'
                    }
                }
            }
        ),
        Tool(
            name='find_price_outliers',
            description='Find products with unusual pricing (significantly higher or lower than average)',
            inputSchema={
                'type': 'object',
                'properties': {
                    'outlier_threshold': {
                        'type': 'number',
                        'default': 2.0,
                        'description': 'Standard deviation threshold for outlier detection'
                    },
                    'category_tag': {
                        'type': 'string',
                        'description': 'Focus on specific category'
                    }
                }
            }
        ),
        Tool(
            name='compare_store_pricing',
            description='Compare pricing strategies across different stores',
            inputSchema={
                'type': 'object',
                'properties': {
                    'store_ids': {
                        'type': 'array',
                        'items': {'type': 'integer'},
                        'description': 'List of store IDs to compare'
                    }
                }
            }
        ),
        Tool(
            name='find_similar_products',
            description='Find products with similar names/descriptions and compare their prices',
            inputSchema={
                'type': 'object',
                'properties': {
                    'product_name': {
                        'type': 'string',
                        'description': 'Product name to find similar products for'
                    },
                    'similarity_threshold': {
                        'type': 'number',
                        'default': 0.7,
                        'description': 'Similarity threshold (0-1)'
                    }
                },
                'required': ['product_name']
            }
        ),
        Tool(
            name='get_market_positioning',
            description='Analyze market positioning based on price points and categories',
            inputSchema={
                'type': 'object',
                'properties': {
                    'store_id': {
                        'type': 'integer',
                        'description': 'Store to analyze positioning for'
                    }
                }
            }
        ),
        Tool(
            name='identify_pricing_gaps',
            description='Identify price gaps and potential pricing opportunities in the market',
            inputSchema={
                'type': 'object',
                'properties': {
                    'category_tag': {
                        'type': 'string',
                        'description': 'Focus on specific category'
                    },
                    'min_gap': {
                        'type': 'number',
                        'default': 10.0,
                        'description': 'Minimum price gap to identify (in currency units)'
                    }
                }
            }
        ),
        Tool(
            name='generate_pricing_recommendations',
            description='Generate pricing recommendations for products or stores',
            inputSchema={
                'type': 'object',
                'properties': {
                    'store_id': {
                        'type': 'integer',
                        'description': 'Store to generate recommendations for'
                    },
                    'product_id': {
                        'type': 'integer',
                        'description': 'Specific product to analyze'
                    }
                }
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[TextContent]:
    """Handle tool calls for price intelligence operations."""
    try:
        if name == 'analyze_price_trends':
            return await _analyze_price_trends(arguments or {})
        elif name == 'find_price_outliers':
            return await _find_price_outliers(arguments or {})
        elif name == 'compare_store_pricing':
            return await _compare_store_pricing(arguments or {})
        elif name == 'find_similar_products':
            return await _find_similar_products(arguments or {})
        elif name == 'get_market_positioning':
            return await _get_market_positioning(arguments or {})
        elif name == 'identify_pricing_gaps':
            return await _identify_pricing_gaps(arguments or {})
        elif name == 'generate_pricing_recommendations':
            return await _generate_pricing_recommendations(arguments or {})
        else:
            return [TextContent(type='text', text=f'Unknown tool: {name}')]
    except Exception as e:
        logger.error(f'Error calling tool {name}: {e}')
        return [TextContent(type='text', text=f'Error: {str(e)}')]


async def _analyze_price_trends(args: Dict[str, Any]) -> List[TextContent]:
    """Analyze price trends across products."""
    category_tag = args.get('category_tag')
    store_id = args.get('store_id')
    
    with get_http_client() as client:
        params = {'limit': 1000}
        if store_id:
            params['store_id'] = store_id
        
        products_response = client.get('/v1/products/', params=params)
        products_response.raise_for_status()
        products = products_response.json()
        
        # Filter by category if specified
        if category_tag:
            products = [p for p in products if p.get('tags') and 
                       any(tag['name'].lower() == category_tag.lower() for tag in p['tags'])]
        
        products_with_prices = [p for p in products if p.get('price') is not None]
        
        if not products_with_prices:
            return [TextContent(type='text', text='No products with prices found for analysis.')]
        
        prices = [float(p['price']) for p in products_with_prices]
        
        result = f'# 📈 Price Trend Analysis{f" - {category_tag}" if category_tag else ""}\\n\\n'
        result += f'**Products Analyzed:** {len(products_with_prices)}\\n\\n'
        
        # Basic statistics
        result += '## Price Statistics\\n'
        result += f'**Price Range:** €{min(prices):.2f} - €{max(prices):.2f}\\n'
        result += f'**Average Price:** €{mean(prices):.2f}\\n'
        result += f'**Median Price:** €{median(prices):.2f}\\n'
        
        # Price distribution
        price_ranges = [
            (0, 10, '€0-10'),
            (10, 25, '€10-25'),
            (25, 50, '€25-50'),
            (50, 100, '€50-100'),
            (100, 250, '€100-250'),
            (250, 500, '€250-500'),
            (500, float('inf'), '€500+')
        ]
        
        result += '\\n**Price Distribution:**\\n'
        for min_price, max_price, label in price_ranges:
            count = sum(1 for p in prices if min_price <= p < max_price)
            if count > 0:
                percentage = count / len(prices) * 100
                result += f'  • {label}: {count} products ({percentage:.1f}%)\\n'
        
        # Store-wise analysis if not filtered by store
        if not store_id:
            store_prices = defaultdict(list)
            for product in products_with_prices:
                if product.get('store_id'):
                    store_prices[product['store_id']].append(float(product['price']))
            
            if len(store_prices) > 1:
                result += '\\n## Store Pricing Analysis\\n'
                stores_response = client.get('/v1/stores/')
                stores_response.raise_for_status()
                stores = {s['id']: s['name'] for s in stores_response.json()}
                
                store_stats = []
                for store_id, store_prices_list in store_prices.items():
                    store_name = stores.get(store_id, f'Store {store_id}')
                    avg_price = mean(store_prices_list)
                    store_stats.append((store_name, avg_price, len(store_prices_list)))
                
                store_stats.sort(key=lambda x: x[1], reverse=True)
                
                result += '**Average Pricing by Store:**\\n'
                for store_name, avg_price, count in store_stats[:10]:
                    result += f'  • {store_name}: €{avg_price:.2f} avg ({count} products)\\n'
        
        return [TextContent(type='text', text=result)]


async def _find_price_outliers(args: Dict[str, Any]) -> List[TextContent]:
    """Find pricing outliers."""
    threshold = args.get('outlier_threshold', 2.0)
    category_tag = args.get('category_tag')
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        # Filter by category if specified
        if category_tag:
            products = [p for p in products if p.get('tags') and 
                       any(tag['name'].lower() == category_tag.lower() for tag in p['tags'])]
        
        products_with_prices = [p for p in products if p.get('price') is not None]
        
        if len(products_with_prices) < 3:
            return [TextContent(type='text', text='Not enough products with prices for outlier analysis.')]
        
        prices = [float(p['price']) for p in products_with_prices]
        avg_price = mean(prices)
        
        # Calculate standard deviation
        variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
        std_dev = variance ** 0.5
        
        # Find outliers
        high_outliers = []
        low_outliers = []
        
        for product in products_with_prices:
            price = float(product['price'])
            z_score = (price - avg_price) / std_dev if std_dev > 0 else 0
            
            if z_score > threshold:
                high_outliers.append((product, price, z_score))
            elif z_score < -threshold:
                low_outliers.append((product, price, z_score))
        
        result = f'# 🎯 Price Outlier Analysis{f" - {category_tag}" if category_tag else ""}\\n\\n'
        result += f'**Analysis Parameters:**\\n'
        result += f'  • Products analyzed: {len(products_with_prices)}\\n'
        result += f'  • Average price: €{avg_price:.2f}\\n'
        result += f'  • Standard deviation: €{std_dev:.2f}\\n'
        result += f'  • Outlier threshold: {threshold}σ\\n\\n'
        
        # High-priced outliers
        if high_outliers:
            high_outliers.sort(key=lambda x: x[2], reverse=True)
            result += f'## 💰 High-Priced Outliers ({len(high_outliers)} found)\\n'
            for product, price, z_score in high_outliers[:10]:
                store_name = product.get('store', {}).get('name', 'Unknown Store') if product.get('store') else 'No Store'
                result += f'• **{product["name"]}** - €{price:.2f} ({z_score:.1f}σ above avg) - {store_name}\\n'
            result += '\\n'
        
        # Low-priced outliers
        if low_outliers:
            low_outliers.sort(key=lambda x: x[2])
            result += f'## 💸 Low-Priced Outliers ({len(low_outliers)} found)\\n'
            for product, price, z_score in low_outliers[:10]:
                store_name = product.get('store', {}).get('name', 'Unknown Store') if product.get('store') else 'No Store'
                result += f'• **{product["name"]}** - €{price:.2f} ({abs(z_score):.1f}σ below avg) - {store_name}\\n'
            result += '\\n'
        
        if not high_outliers and not low_outliers:
            result += 'No significant price outliers found with the specified threshold.\\n'
        
        return [TextContent(type='text', text=result)]


async def _compare_store_pricing(args: Dict[str, Any]) -> List[TextContent]:
    """Compare pricing strategies across stores."""
    store_ids = args.get('store_ids', [])
    
    with get_http_client() as client:
        if not store_ids:
            # Get all stores if none specified
            stores_response = client.get('/v1/stores/')
            stores_response.raise_for_status()
            stores_data = stores_response.json()
            store_ids = [s['id'] for s in stores_data[:5]]  # Limit to 5 stores
        
        # Get products for all stores
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        # Get store details
        stores_response = client.get('/v1/stores/')
        stores_response.raise_for_status()
        stores = {s['id']: s for s in stores_response.json()}
        
        result = f'# 🏪 Store Pricing Comparison ({len(store_ids)} stores)\\n\\n'
        
        store_analyses = []
        
        for store_id in store_ids:
            if store_id not in stores:
                continue
                
            store = stores[store_id]
            store_products = [p for p in products if p.get('store_id') == store_id and p.get('price')]
            
            if not store_products:
                continue
            
            prices = [float(p['price']) for p in store_products]
            
            analysis = {
                'name': store['name'],
                'type': store.get('type', 'unknown'),
                'product_count': len(store_products),
                'avg_price': mean(prices),
                'median_price': median(prices),
                'min_price': min(prices),
                'max_price': max(prices),
                'price_range': max(prices) - min(prices)
            }
            store_analyses.append(analysis)
        
        if not store_analyses:
            return [TextContent(type='text', text='No stores found with priced products for comparison.')]
        
        # Sort by average price
        store_analyses.sort(key=lambda x: x['avg_price'], reverse=True)
        
        result += '## Pricing Overview\\n'
        result += '| Store | Type | Products | Avg Price | Price Range |\\n'
        result += '|-------|------|----------|-----------|-------------|\\n'
        
        for analysis in store_analyses:
            result += f'| {analysis["name"]} | {analysis["type"]} | {analysis["product_count"]} | €{analysis["avg_price"]:.2f} | €{analysis["min_price"]:.2f}-€{analysis["max_price"]:.2f} |\\n'
        
        # Pricing strategy analysis
        result += '\\n## Pricing Strategy Analysis\\n\\n'
        
        highest_avg = store_analyses[0]
        lowest_avg = store_analyses[-1]
        
        result += f'**Premium Positioning:** {highest_avg["name"]} (€{highest_avg["avg_price"]:.2f} avg)\\n'
        result += f'**Budget Positioning:** {lowest_avg["name"]} (€{lowest_avg["avg_price"]:.2f} avg)\\n\\n'
        
        # Price spread analysis
        most_varied = max(store_analyses, key=lambda x: x['price_range'])
        least_varied = min(store_analyses, key=lambda x: x['price_range'])
        
        result += f'**Most Price Varied:** {most_varied["name"]} (€{most_varied["price_range"]:.2f} range)\\n'
        result += f'**Most Consistent:** {least_varied["name"]} (€{least_varied["price_range"]:.2f} range)\\n\\n'
        
        # Market positioning
        all_avg_prices = [s['avg_price'] for s in store_analyses]
        market_avg = mean(all_avg_prices)
        
        result += f'**Market Average:** €{market_avg:.2f}\\n\\n'
        result += '**Market Positioning:**\\n'
        for analysis in store_analyses:
            if analysis['avg_price'] > market_avg * 1.2:
                positioning = 'Premium (>20% above market)'
            elif analysis['avg_price'] > market_avg * 1.1:
                positioning = 'Above Market (>10% above)'
            elif analysis['avg_price'] < market_avg * 0.8:
                positioning = 'Budget (<20% below market)'
            elif analysis['avg_price'] < market_avg * 0.9:
                positioning = 'Below Market (<10% below)'
            else:
                positioning = 'Market Average'
            
            result += f'  • {analysis["name"]}: {positioning}\\n'
        
        return [TextContent(type='text', text=result)]


async def _find_similar_products(args: Dict[str, Any]) -> List[TextContent]:
    """Find similar products and compare prices."""
    product_name = args.get('product_name', '').lower()
    threshold = args.get('similarity_threshold', 0.7)
    
    if not product_name:
        return [TextContent(type='text', text='Error: product_name is required')]
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        # Simple similarity function based on common words
        def calculate_similarity(name1, name2):
            words1 = set(re.findall(r'\\w+', name1.lower()))
            words2 = set(re.findall(r'\\w+', name2.lower()))
            if not words1 or not words2:
                return 0
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            return len(intersection) / len(union) if union else 0
        
        # Find similar products
        similar_products = []
        for product in products:
            similarity = calculate_similarity(product_name, product['name'])
            if similarity >= threshold:
                similar_products.append((product, similarity))
        
        if not similar_products:
            return [TextContent(type='text', text=f'No similar products found for "{product_name}" with similarity threshold {threshold}.')]
        
        # Sort by similarity
        similar_products.sort(key=lambda x: x[1], reverse=True)
        
        result = f'# 🔍 Similar Products to "{product_name}"\\n\\n'
        result += f'**Found {len(similar_products)} similar products** (similarity ≥ {threshold})\\n\\n'
        
        # Products with prices for comparison
        priced_products = [(p, sim) for p, sim in similar_products if p.get('price')]
        
        if priced_products:
            prices = [float(p['price']) for p, _ in priced_products]
            result += f'## Price Comparison ({len(priced_products)} with prices)\\n'
            result += f'**Price Range:** €{min(prices):.2f} - €{max(prices):.2f}\\n'
            result += f'**Average Price:** €{mean(prices):.2f}\\n\\n'
        
        result += '## Product List\\n'
        for product, similarity in similar_products[:15]:
            store_name = product.get('store', {}).get('name', 'Unknown') if product.get('store') else 'No Store'
            price_str = f'€{product["price"]}' if product.get('price') else 'No price'
            
            result += f'• **{product["name"]}** ({similarity:.0%} similar)\\n'
            result += f'  Price: {price_str} | Store: {store_name} | ID: {product["id"]}\\n\\n'
        
        if len(similar_products) > 15:
            result += f'... and {len(similar_products) - 15} more similar products.\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_market_positioning(args: Dict[str, Any]) -> List[TextContent]:
    """Analyze market positioning for a store."""
    store_id = args.get('store_id')
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        all_products = products_response.json()
        
        if store_id:
            # Analyze specific store
            store_response = client.get(f'/v1/stores/{store_id}')
            if store_response.status_code == 404:
                return [TextContent(type='text', text=f'Store with ID {store_id} not found.')]
            store_response.raise_for_status()
            store = store_response.json()
            
            store_products = [p for p in all_products if p.get('store_id') == store_id and p.get('price')]
            market_products = [p for p in all_products if p.get('price') and p.get('store_id') != store_id]
            
            if not store_products:
                return [TextContent(type='text', text=f'No priced products found for {store["name"]}.')]
            
            result = f'# 📊 Market Positioning Analysis - {store["name"]}\\n\\n'
        else:
            # Overall market analysis
            market_products = [p for p in all_products if p.get('price')]
            result = f'# 📊 Overall Market Positioning Analysis\\n\\n'
        
        if store_id:
            store_prices = [float(p['price']) for p in store_products]
            market_prices = [float(p['price']) for p in market_products]
            
            if not market_products:
                return [TextContent(type='text', text='No other priced products in market for comparison.')]
            
            store_avg = mean(store_prices)
            market_avg = mean(market_prices)
            
            result += f'## Pricing Position\\n'
            result += f'**Store Average Price:** €{store_avg:.2f}\\n'
            result += f'**Market Average Price:** €{market_avg:.2f}\\n'
            result += f'**Price Premium/Discount:** {(store_avg - market_avg) / market_avg * 100:+.1f}%\\n\\n'
            
            # Position classification
            if store_avg > market_avg * 1.3:
                position = 'Ultra Premium'
            elif store_avg > market_avg * 1.15:
                position = 'Premium'
            elif store_avg > market_avg * 1.05:
                position = 'Above Market'
            elif store_avg < market_avg * 0.7:
                position = 'Ultra Budget'
            elif store_avg < market_avg * 0.85:
                position = 'Budget'
            elif store_avg < market_avg * 0.95:
                position = 'Below Market'
            else:
                position = 'Market Average'
            
            result += f'**Market Position:** {position}\\n\\n'
            
            # Category analysis
            store_tags = []
            for product in store_products:
                if product.get('tags'):
                    store_tags.extend([tag['name'] for tag in product['tags']])
            
            if store_tags:
                category_counts = Counter(store_tags)
                result += f'## Category Focus\\n'
                result += f'**Top Categories:**\\n'
                for category, count in category_counts.most_common(5):
                    percentage = count / len(store_products) * 100
                    result += f'  • {category}: {count} products ({percentage:.1f}%)\\n'
        
        else:
            # Overall market structure
            all_prices = [float(p['price']) for p in market_products]
            result += f'**Total Products with Prices:** {len(market_products)}\\n'
            result += f'**Market Price Range:** €{min(all_prices):.2f} - €{max(all_prices):.2f}\\n'
            result += f'**Market Average:** €{mean(all_prices):.2f}\\n'
            result += f'**Market Median:** €{median(all_prices):.2f}\\n\\n'
            
            # Market segments
            segments = [
                (0, 25, 'Budget'),
                (25, 75, 'Mid-Range'),
                (75, 200, 'Premium'),
                (200, float('inf'), 'Luxury')
            ]
            
            result += '## Market Segments\\n'
            for min_price, max_price, segment in segments:
                count = sum(1 for p in all_prices if min_price <= p < max_price)
                if count > 0:
                    avg_segment = mean([p for p in all_prices if min_price <= p < max_price])
                    percentage = count / len(all_prices) * 100
                    result += f'**{segment} (€{min_price}-{max_price if max_price != float("inf") else "∞"}):** {count} products ({percentage:.1f}%), avg €{avg_segment:.2f}\\n'
        
        return [TextContent(type='text', text=result)]


async def _identify_pricing_gaps(args: Dict[str, Any]) -> List[TextContent]:
    """Identify pricing gaps in the market."""
    category_tag = args.get('category_tag')
    min_gap = args.get('min_gap', 10.0)
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        # Filter by category if specified
        if category_tag:
            products = [p for p in products if p.get('tags') and 
                       any(tag['name'].lower() == category_tag.lower() for tag in p['tags'])]
        
        products_with_prices = [p for p in products if p.get('price') is not None]
        
        if len(products_with_prices) < 2:
            return [TextContent(type='text', text='Not enough products with prices to identify gaps.')]
        
        prices = sorted(set(float(p['price']) for p in products_with_prices))
        
        # Find gaps
        gaps = []
        for i in range(len(prices) - 1):
            gap_size = prices[i + 1] - prices[i]
            if gap_size >= min_gap:
                gaps.append((prices[i], prices[i + 1], gap_size))
        
        result = f'# 🔍 Pricing Gap Analysis{f" - {category_tag}" if category_tag else ""}\\n\\n'
        result += f'**Products Analyzed:** {len(products_with_prices)}\\n'
        result += f'**Unique Price Points:** {len(prices)}\\n'
        result += f'**Minimum Gap Size:** €{min_gap}\\n\\n'
        
        if not gaps:
            result += f'No pricing gaps of €{min_gap} or larger found.\\n'
            
            # Show smaller gaps if no large ones found
            smaller_gaps = []
            for i in range(len(prices) - 1):
                gap_size = prices[i + 1] - prices[i]
                if gap_size >= 5.0:  # Show gaps of €5 or more
                    smaller_gaps.append((prices[i], prices[i + 1], gap_size))
            
            if smaller_gaps:
                result += f'\\n**Smaller Gaps (€5+):**\\n'
                for low, high, gap in smaller_gaps[:5]:
                    result += f'  • €{low:.2f} to €{high:.2f} (gap: €{gap:.2f})\\n'
        else:
            result += f'## Identified Pricing Gaps ({len(gaps)} found)\\n\\n'
            
            # Sort by gap size
            gaps.sort(key=lambda x: x[2], reverse=True)
            
            for i, (low_price, high_price, gap_size) in enumerate(gaps[:10], 1):
                result += f'{i}. **€{low_price:.2f} to €{high_price:.2f}**\\n'
                result += f'   Gap Size: €{gap_size:.2f}\\n'
                
                # Find products around this gap
                products_below = [p for p in products_with_prices 
                                if abs(float(p['price']) - low_price) < 1.0]
                products_above = [p for p in products_with_prices 
                                if abs(float(p['price']) - high_price) < 1.0]
                
                if products_below:
                    result += f'   Products below gap: {products_below[0]["name"]} (€{products_below[0]["price"]})\\n'
                if products_above:
                    result += f'   Products above gap: {products_above[0]["name"]} (€{products_above[0]["price"]})\\n'
                
                result += '\\n'
            
            if len(gaps) > 10:
                result += f'... and {len(gaps) - 10} more gaps.\\n'
        
        # Market opportunity assessment
        if gaps:
            total_gap_value = sum(gap[2] for gap in gaps)
            largest_gap = max(gaps, key=lambda x: x[2])
            
            result += '\\n## Market Opportunities\\n'
            result += f'**Total Gap Value:** €{total_gap_value:.2f}\\n'
            result += f'**Largest Opportunity:** €{largest_gap[0]:.2f} - €{largest_gap[1]:.2f} (€{largest_gap[2]:.2f} gap)\\n'
            
            mid_range_gaps = [g for g in gaps if 25 <= g[0] <= 200]  # Focus on mid-range
            if mid_range_gaps:
                result += f'**Mid-Range Opportunities:** {len(mid_range_gaps)} gaps in €25-200 range\\n'
        
        return [TextContent(type='text', text=result)]


async def _generate_pricing_recommendations(args: Dict[str, Any]) -> List[TextContent]:
    """Generate pricing recommendations."""
    store_id = args.get('store_id')
    product_id = args.get('product_id')
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        all_products = products_response.json()
        
        if product_id:
            # Recommendations for specific product
            target_product = next((p for p in all_products if p['id'] == product_id), None)
            if not target_product:
                return [TextContent(type='text', text=f'Product with ID {product_id} not found.')]
            
            result = f'# 💡 Pricing Recommendations - {target_product["name"]}\\n\\n'
            
            # Find similar products by name/tags
            similar_products = []
            if target_product.get('tags'):
                target_tags = set(tag['name'] for tag in target_product['tags'])
                for product in all_products:
                    if product['id'] == product_id or not product.get('price'):
                        continue
                    if product.get('tags'):
                        product_tags = set(tag['name'] for tag in product['tags'])
                        if target_tags.intersection(product_tags):
                            similar_products.append(product)
            
            if similar_products:
                similar_prices = [float(p['price']) for p in similar_products]
                avg_similar = mean(similar_prices)
                median_similar = median(similar_prices)
                
                result += f'## Market Context\\n'
                result += f'**Similar Products Found:** {len(similar_products)}\\n'
                result += f'**Similar Products Price Range:** €{min(similar_prices):.2f} - €{max(similar_prices):.2f}\\n'
                result += f'**Average of Similar:** €{avg_similar:.2f}\\n'
                result += f'**Median of Similar:** €{median_similar:.2f}\\n\\n'
                
                current_price = float(target_product['price']) if target_product.get('price') else None
                
                result += f'## Recommendations\\n'
                if current_price:
                    result += f'**Current Price:** €{current_price:.2f}\\n'
                    if current_price > avg_similar * 1.2:
                        result += f'**Status:** Overpriced (20% above similar products)\\n'
                        result += f'**Recommendation:** Consider reducing to €{avg_similar * 1.1:.2f} (10% premium)\\n'
                    elif current_price < avg_similar * 0.8:
                        result += f'**Status:** Underpriced (20% below similar products)\\n'
                        result += f'**Recommendation:** Consider increasing to €{avg_similar * 0.9:.2f} (10% discount to market)\\n'
                    else:
                        result += f'**Status:** Competitively priced\\n'
                        result += f'**Recommendation:** Current pricing is appropriate\\n'
                else:
                    result += f'**Current Status:** No price set\\n'
                    result += f'**Suggested Price Range:** €{avg_similar * 0.9:.2f} - €{avg_similar * 1.1:.2f}\\n'
                    result += f'**Conservative Price:** €{median_similar:.2f}\\n'
            else:
                result += 'No similar products found for comparison. Consider market research for this unique product.\\n'
        
        elif store_id:
            # Recommendations for entire store
            store_response = client.get(f'/v1/stores/{store_id}')
            if store_response.status_code == 404:
                return [TextContent(type='text', text=f'Store with ID {store_id} not found.')]
            store_response.raise_for_status()
            store = store_response.json()
            
            store_products = [p for p in all_products if p.get('store_id') == store_id]
            store_priced = [p for p in store_products if p.get('price')]
            market_products = [p for p in all_products if p.get('price') and p.get('store_id') != store_id]
            
            if not store_priced:
                return [TextContent(type='text', text=f'No priced products found for {store["name"]}.')]
            
            result = f'# 💡 Store Pricing Recommendations - {store["name"]}\\n\\n'
            
            store_prices = [float(p['price']) for p in store_priced]
            market_prices = [float(p['price']) for p in market_products]
            
            store_avg = mean(store_prices)
            market_avg = mean(market_prices)
            
            result += f'## Current Position\\n'
            result += f'**Store Average:** €{store_avg:.2f}\\n'
            result += f'**Market Average:** €{market_avg:.2f}\\n'
            result += f'**Position:** {(store_avg - market_avg) / market_avg * 100:+.1f}% vs market\\n\\n'
            
            result += f'## Recommendations\\n'
            
            # Identify overpriced/underpriced products
            overpriced = []
            underpriced = []
            
            for product in store_priced:
                # Find similar products in market
                similar_market = []
                if product.get('tags'):
                    product_tags = set(tag['name'] for tag in product['tags'])
                    for market_product in market_products:
                        if market_product.get('tags'):
                            market_tags = set(tag['name'] for tag in market_product['tags'])
                            if product_tags.intersection(market_tags):
                                similar_market.append(market_product)
                
                if similar_market and len(similar_market) >= 2:
                    similar_prices = [float(p['price']) for p in similar_market]
                    similar_avg = mean(similar_prices)
                    product_price = float(product['price'])
                    
                    if product_price > similar_avg * 1.3:
                        overpriced.append((product, product_price, similar_avg))
                    elif product_price < similar_avg * 0.7:
                        underpriced.append((product, product_price, similar_avg))
            
            if overpriced:
                result += f'**High Priority - Overpriced Products ({len(overpriced)}):**\\n'
                for product, current, market_avg in overpriced[:5]:
                    result += f'  • {product["name"]}: €{current:.2f} → €{market_avg * 1.1:.2f} (market +10%)\\n'
                result += '\\n'
            
            if underpriced:
                result += f'**Revenue Opportunity - Underpriced Products ({len(underpriced)}):**\\n'
                for product, current, market_avg in underpriced[:5]:
                    result += f'  • {product["name"]}: €{current:.2f} → €{market_avg * 0.9:.2f} (market -10%)\\n'
                result += '\\n'
            
            # Products without prices
            unpriced = [p for p in store_products if not p.get('price')]
            if unpriced:
                result += f'**Missing Prices ({len(unpriced)} products):**\\n'
                result += f'Priority: Set prices for products to increase revenue potential.\\n\\n'
            
            # Overall strategy recommendation
            if store_avg > market_avg * 1.2:
                result += f'**Strategy:** Premium positioning - justify high prices with quality/service\\n'
            elif store_avg < market_avg * 0.8:
                result += f'**Strategy:** Budget positioning - ensure costs allow for sustainable margins\\n'
            else:
                result += f'**Strategy:** Competitive positioning - focus on differentiation\\n'
        
        else:
            return [TextContent(type='text', text='Error: Either store_id or product_id must be provided.')]
        
        return [TextContent(type='text', text=result)]


if __name__ == '__main__':
    # This will be called by the run script
    logger.info('Starting Partle Price Intelligence MCP Server')
    mcp_server.run()
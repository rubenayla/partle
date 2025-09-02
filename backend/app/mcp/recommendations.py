"""MCP Server for Partle Recommendations and Personalization."""
import logging
from typing import Optional, Any, Dict, List
from contextlib import contextmanager
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import json
import os
from collections import defaultdict, Counter
import math
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
API_BASE_URL = os.getenv('PARTLE_API_URL', 'http://localhost:8000')

# Initialize MCP server
mcp_server = Server('partle-recommendations')


@contextmanager
def get_http_client():
    """Get HTTP client for API requests."""
    with httpx.Client(base_url=API_BASE_URL) as client:
        yield client


def calculate_similarity_score(product1: Dict, product2: Dict) -> float:
    """Calculate similarity between two products based on tags, price, and store."""
    score = 0.0
    
    # Tag similarity (40% weight)
    if product1.get('tags') and product2.get('tags'):
        tags1 = set(tag['name'] for tag in product1['tags'])
        tags2 = set(tag['name'] for tag in product2['tags'])
        if tags1 or tags2:
            intersection = tags1.intersection(tags2)
            union = tags1.union(tags2)
            tag_similarity = len(intersection) / len(union) if union else 0
            score += tag_similarity * 0.4
    
    # Price similarity (30% weight)
    if product1.get('price') and product2.get('price'):
        price1, price2 = float(product1['price']), float(product2['price'])
        price_diff = abs(price1 - price2)
        max_price = max(price1, price2)
        if max_price > 0:
            price_similarity = 1 - min(price_diff / max_price, 1)
            score += price_similarity * 0.3
    
    # Store similarity (20% weight)
    if product1.get('store_id') and product2.get('store_id'):
        if product1['store_id'] == product2['store_id']:
            score += 0.2
    
    # Name similarity (10% weight) - simple word overlap
    name1 = set(product1['name'].lower().split())
    name2 = set(product2['name'].lower().split())
    if name1 or name2:
        name_intersection = name1.intersection(name2)
        name_union = name1.union(name2)
        name_similarity = len(name_intersection) / len(name_union) if name_union else 0
        score += name_similarity * 0.1
    
    return score


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for recommendations."""
    return [
        Tool(
            name='recommend_similar_products',
            description='Find products similar to a given product based on tags, price, and characteristics',
            inputSchema={
                'type': 'object',
                'properties': {
                    'product_id': {
                        'type': 'integer',
                        'description': 'ID of the product to find similar items for'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 10,
                        'description': 'Maximum number of recommendations to return'
                    },
                    'min_similarity_score': {
                        'type': 'number',
                        'default': 0.3,
                        'description': 'Minimum similarity score (0-1) for recommendations'
                    },
                    'include_same_store': {
                        'type': 'boolean',
                        'default': True,
                        'description': 'Include products from the same store'
                    }
                },
                'required': ['product_id']
            }
        ),
        Tool(
            name='recommend_products_by_category',
            description='Recommend products based on category/tag preferences',
            inputSchema={
                'type': 'object',
                'properties': {
                    'tags': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'List of preferred tags/categories'
                    },
                    'price_range': {
                        'type': 'object',
                        'properties': {
                            'min_price': {'type': 'number'},
                            'max_price': {'type': 'number'}
                        },
                        'description': 'Preferred price range'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 15,
                        'description': 'Maximum number of recommendations'
                    }
                },
                'required': ['tags']
            }
        ),
        Tool(
            name='recommend_stores_by_products',
            description='Recommend stores based on the types of products they offer',
            inputSchema={
                'type': 'object',
                'properties': {
                    'preferred_categories': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'Preferred product categories/tags'
                    },
                    'location': {
                        'type': 'object',
                        'properties': {
                            'lat': {'type': 'number'},
                            'lon': {'type': 'number'},
                            'radius_km': {'type': 'number', 'default': 10}
                        },
                        'description': 'Location preference for store recommendations'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 10,
                        'description': 'Maximum number of store recommendations'
                    }
                },
                'required': ['preferred_categories']
            }
        ),
        Tool(
            name='get_trending_products',
            description='Get trending/popular products based on various metrics',
            inputSchema={
                'type': 'object',
                'properties': {
                    'metric': {
                        'type': 'string',
                        'enum': ['recent', 'high_value', 'popular_tags', 'price_gaps'],
                        'default': 'recent',
                        'description': 'Trending metric to use'
                    },
                    'category_filter': {
                        'type': 'string',
                        'description': 'Filter by specific category/tag'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 20,
                        'description': 'Maximum number of trending products'
                    }
                }
            }
        ),
        Tool(
            name='recommend_complementary_products',
            description='Recommend products that complement or pair well with a given product',
            inputSchema={
                'type': 'object',
                'properties': {
                    'product_id': {
                        'type': 'integer',
                        'description': 'ID of the base product'
                    },
                    'complementary_logic': {
                        'type': 'string',
                        'enum': ['different_category', 'price_tier', 'store_variety'],
                        'default': 'different_category',
                        'description': 'Logic for finding complementary products'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 8,
                        'description': 'Maximum number of complementary recommendations'
                    }
                },
                'required': ['product_id']
            }
        ),
        Tool(
            name='generate_shopping_list',
            description='Generate a curated shopping list based on preferences and constraints',
            inputSchema={
                'type': 'object',
                'properties': {
                    'budget': {
                        'type': 'number',
                        'description': 'Maximum budget for the shopping list'
                    },
                    'categories': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'Required/preferred categories to include'
                    },
                    'store_preference': {
                        'type': 'string',
                        'enum': ['single_store', 'multiple_stores', 'online_only', 'physical_only'],
                        'default': 'multiple_stores',
                        'description': 'Store selection strategy'
                    },
                    'optimization_goal': {
                        'type': 'string',
                        'enum': ['lowest_price', 'best_variety', 'convenience'],
                        'default': 'best_variety',
                        'description': 'Primary optimization goal'
                    }
                }
            }
        ),
        Tool(
            name='recommend_price_alerts',
            description='Recommend products to set price alerts for based on market analysis',
            inputSchema={
                'type': 'object',
                'properties': {
                    'categories': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'Categories of interest for price alerts'
                    },
                    'alert_type': {
                        'type': 'string',
                        'enum': ['overpriced', 'underpriced', 'price_drops', 'new_products'],
                        'default': 'price_drops',
                        'description': 'Type of price alerts to recommend'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 15,
                        'description': 'Maximum number of alert recommendations'
                    }
                }
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[TextContent]:
    """Handle tool calls for recommendation operations."""
    try:
        if name == 'recommend_similar_products':
            return await _recommend_similar_products(arguments or {})
        elif name == 'recommend_products_by_category':
            return await _recommend_products_by_category(arguments or {})
        elif name == 'recommend_stores_by_products':
            return await _recommend_stores_by_products(arguments or {})
        elif name == 'get_trending_products':
            return await _get_trending_products(arguments or {})
        elif name == 'recommend_complementary_products':
            return await _recommend_complementary_products(arguments or {})
        elif name == 'generate_shopping_list':
            return await _generate_shopping_list(arguments or {})
        elif name == 'recommend_price_alerts':
            return await _recommend_price_alerts(arguments or {})
        else:
            return [TextContent(type='text', text=f'Unknown tool: {name}')]
    except Exception as e:
        logger.error(f'Error calling tool {name}: {e}')
        return [TextContent(type='text', text=f'Error: {str(e)}')]


async def _recommend_similar_products(args: Dict[str, Any]) -> List[TextContent]:
    """Recommend products similar to a given product."""
    product_id = args.get('product_id')
    limit = args.get('limit', 10)
    min_similarity = args.get('min_similarity_score', 0.3)
    include_same_store = args.get('include_same_store', True)
    
    if not product_id:
        return [TextContent(type='text', text='Error: product_id is required')]
    
    with get_http_client() as client:
        # Get the target product
        target_response = client.get(f'/v1/products/{product_id}')
        if target_response.status_code == 404:
            return [TextContent(type='text', text=f'Product with ID {product_id} not found.')]
        target_response.raise_for_status()
        target_product = target_response.json()
        
        # Get all products for comparison
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        all_products = products_response.json()
        
        # Calculate similarities
        similarities = []
        for product in all_products:
            if product['id'] == product_id:
                continue  # Skip the target product itself
            
            if not include_same_store and product.get('store_id') == target_product.get('store_id'):
                continue
            
            similarity = calculate_similarity_score(target_product, product)
            if similarity >= min_similarity:
                similarities.append((product, similarity))
        
        # Sort by similarity score
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        result = f'# 🔍 Similar Products to "{target_product["name"]}"\\n\\n'
        result += f'**Target Product:** {target_product["name"]}\\n'
        if target_product.get('price'):
            result += f'**Target Price:** €{target_product["price"]}\\n'
        if target_product.get('tags'):
            target_tags = [tag['name'] for tag in target_product['tags']]
            result += f'**Target Categories:** {", ".join(target_tags)}\\n'
        result += f'**Minimum Similarity:** {min_similarity:.2f}\\n\\n'
        
        if not similarities:
            result += 'No similar products found with the specified criteria.\\n'
            result += 'Try lowering the minimum similarity score or expanding the search parameters.\\n'
            return [TextContent(type='text', text=result)]
        
        result += f'**Similar Products Found:** {len(similarities)}\\n\\n'
        
        # Show recommendations
        for i, (product, similarity) in enumerate(similarities[:limit], 1):
            result += f'{i}. **{product["name"]}** (similarity: {similarity:.2f})\\n'
            
            if product.get('price'):
                result += f'   Price: €{product["price"]}'
                if target_product.get('price'):
                    price_diff = float(product['price']) - float(target_product['price'])
                    result += f' ({price_diff:+.2f}€ vs target)'
                result += '\\n'
            
            if product.get('store'):
                result += f'   Store: {product["store"]["name"]}\\n'
            
            if product.get('tags'):
                product_tags = [tag['name'] for tag in product['tags']]
                result += f'   Categories: {", ".join(product_tags)}\\n'
            
            result += f'   ID: {product["id"]}\\n\\n'
        
        if len(similarities) > limit:
            result += f'... and {len(similarities) - limit} more similar products.\\n'
        
        # Analysis summary
        avg_similarity = sum(sim for _, sim in similarities) / len(similarities)
        result += f'\\n**Analysis Summary:**\\n'
        result += f'  • Average similarity score: {avg_similarity:.2f}\\n'
        result += f'  • Products shown: {min(len(similarities), limit)}\\n'
        
        return [TextContent(type='text', text=result)]


async def _recommend_products_by_category(args: Dict[str, Any]) -> List[TextContent]:
    """Recommend products based on category preferences."""
    tags = args.get('tags', [])
    price_range = args.get('price_range', {})
    limit = args.get('limit', 15)
    
    if not tags:
        return [TextContent(type='text', text='Error: tags list is required')]
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        # Filter products by tags
        matching_products = []
        for product in products:
            if product.get('tags'):
                product_tags = set(tag['name'].lower() for tag in product['tags'])
                preferred_tags = set(tag.lower() for tag in tags)
                
                # Calculate tag match score
                intersection = product_tags.intersection(preferred_tags)
                if intersection:
                    tag_score = len(intersection) / len(preferred_tags)
                    matching_products.append((product, tag_score))
        
        # Apply price filter if specified
        if price_range:
            min_price = price_range.get('min_price')
            max_price = price_range.get('max_price')
            
            filtered_products = []
            for product, score in matching_products:
                if product.get('price'):
                    price = float(product['price'])
                    if ((min_price is None or price >= min_price) and 
                        (max_price is None or price <= max_price)):
                        filtered_products.append((product, score))
            matching_products = filtered_products
        
        # Sort by tag match score
        matching_products.sort(key=lambda x: x[1], reverse=True)
        
        result = f'# 🎯 Category-Based Product Recommendations\\n\\n'
        result += f'**Preferred Categories:** {", ".join(tags)}\\n'
        
        if price_range:
            if price_range.get('min_price') is not None:
                result += f'**Min Price:** €{price_range["min_price"]}\\n'
            if price_range.get('max_price') is not None:
                result += f'**Max Price:** €{price_range["max_price"]}\\n'
        
        result += f'**Products Found:** {len(matching_products)}\\n\\n'
        
        if not matching_products:
            result += 'No products found matching your category preferences.\\n'
            return [TextContent(type='text', text=result)]
        
        # Group by tag match score
        perfect_matches = [(p, s) for p, s in matching_products if s == 1.0]
        good_matches = [(p, s) for p, s in matching_products if 0.5 <= s < 1.0]
        partial_matches = [(p, s) for p, s in matching_products if s < 0.5]
        
        if perfect_matches:
            result += f'## Perfect Matches ({len(perfect_matches)} products)\\n'
            for i, (product, score) in enumerate(perfect_matches[:limit//2], 1):
                result += f'{i}. **{product["name"]}**\\n'
                if product.get('price'):
                    result += f'   Price: €{product["price"]}\\n'
                if product.get('store'):
                    result += f'   Store: {product["store"]["name"]}\\n'
                product_tags = [tag['name'] for tag in product['tags']]
                result += f'   Categories: {", ".join(product_tags)}\\n'
                result += f'   ID: {product["id"]}\\n\\n'
        
        if good_matches and len(perfect_matches) < limit:
            remaining_limit = limit - len(perfect_matches)
            result += f'## Good Matches ({len(good_matches)} products)\\n'
            for i, (product, score) in enumerate(good_matches[:remaining_limit], 1):
                result += f'{i}. **{product["name"]}** (match: {score:.0%})\\n'
                if product.get('price'):
                    result += f'   Price: €{product["price"]}\\n'
                if product.get('store'):
                    result += f'   Store: {product["store"]["name"]}\\n'
                product_tags = [tag['name'] for tag in product['tags']]
                result += f'   Categories: {", ".join(product_tags)}\\n'
                result += f'   ID: {product["id"]}\\n\\n'
        
        # Category analysis
        all_tags = []
        for product, _ in matching_products:
            if product.get('tags'):
                all_tags.extend([tag['name'] for tag in product['tags']])
        
        if all_tags:
            category_distribution = Counter(all_tags)
            result += f'## Category Distribution\\n'
            for category, count in category_distribution.most_common(5):
                result += f'  • {category}: {count} products\\n'
        
        return [TextContent(type='text', text=result)]


async def _recommend_stores_by_products(args: Dict[str, Any]) -> List[TextContent]:
    """Recommend stores based on product categories."""
    preferred_categories = args.get('preferred_categories', [])
    location = args.get('location')
    limit = args.get('limit', 10)
    
    if not preferred_categories:
        return [TextContent(type='text', text='Error: preferred_categories is required')]
    
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        products_response = client.get('/v1/products/', params={'limit': 1000})
        
        stores_response.raise_for_status()
        products_response.raise_for_status()
        
        stores = stores_response.json()
        products = products_response.json()
        
        # Analyze products by store and calculate category matches
        store_analysis = defaultdict(lambda: {
            'store': None, 'products': [], 'category_matches': 0, 
            'total_products': 0, 'distance': float('inf')
        })
        
        for product in products:
            if product.get('store_id'):
                store_id = product['store_id']
                store_analysis[store_id]['products'].append(product)
                store_analysis[store_id]['total_products'] += 1
                
                # Check category matches
                if product.get('tags'):
                    product_tags = set(tag['name'].lower() for tag in product['tags'])
                    preferred_tags = set(cat.lower() for cat in preferred_categories)
                    if product_tags.intersection(preferred_tags):
                        store_analysis[store_id]['category_matches'] += 1
        
        # Add store information and location data
        for store in stores:
            if store['id'] in store_analysis:
                store_analysis[store['id']]['store'] = store
                
                # Calculate distance if location provided
                if (location and store.get('lat') and store.get('lon')):
                    from math import sqrt, sin, cos, radians, asin
                    
                    lat1, lon1 = radians(location['lat']), radians(location['lon'])
                    lat2, lon2 = radians(store['lat']), radians(store['lon'])
                    
                    # Haversine formula
                    dlat, dlon = lat2 - lat1, lon2 - lon1
                    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                    distance = 6371 * 2 * asin(sqrt(a))  # Earth radius in km
                    
                    store_analysis[store['id']]['distance'] = distance
        
        # Filter stores with category matches and sort by relevance
        relevant_stores = []
        for store_id, analysis in store_analysis.items():
            if analysis['category_matches'] > 0 and analysis['store']:
                # Calculate relevance score
                category_score = analysis['category_matches'] / analysis['total_products']
                
                # Apply location boost if within radius
                location_score = 1.0
                if location and analysis['distance'] != float('inf'):
                    max_distance = location.get('radius_km', 10)
                    if analysis['distance'] <= max_distance:
                        location_score = 1 + (1 - analysis['distance'] / max_distance) * 0.5
                
                relevance_score = category_score * location_score
                relevant_stores.append((analysis, relevance_score))
        
        # Sort by relevance score
        relevant_stores.sort(key=lambda x: x[1], reverse=True)
        
        result = f'# 🏪 Store Recommendations\\n\\n'
        result += f'**Preferred Categories:** {", ".join(preferred_categories)}\\n'
        
        if location:
            result += f'**Location:** {location["lat"]:.4f}, {location["lon"]:.4f}\\n'
            result += f'**Search Radius:** {location.get("radius_km", 10)}km\\n'
        
        result += f'**Relevant Stores Found:** {len(relevant_stores)}\\n\\n'
        
        if not relevant_stores:
            result += 'No stores found with products matching your preferred categories.\\n'
            return [TextContent(type='text', text=result)]
        
        # Show store recommendations
        for i, (analysis, score) in enumerate(relevant_stores[:limit], 1):
            store = analysis['store']
            result += f'{i}. **{store["name"]}** ({store["type"]})\\n'
            
            # Category match info
            match_percentage = analysis['category_matches'] / analysis['total_products'] * 100
            result += f'   Category Match: {analysis["category_matches"]} of {analysis["total_products"]} products ({match_percentage:.1f}%)\\n'
            
            # Location info
            if analysis['distance'] != float('inf'):
                result += f'   Distance: {analysis["distance"]:.1f}km\\n'
            
            if store.get('address'):
                result += f'   Address: {store["address"]}\\n'
            
            if store.get('homepage'):
                result += f'   Website: {store["homepage"]}\\n'
            
            # Show matching product examples
            matching_products = []
            for product in analysis['products']:
                if product.get('tags'):
                    product_tags = set(tag['name'].lower() for tag in product['tags'])
                    preferred_tags = set(cat.lower() for cat in preferred_categories)
                    if product_tags.intersection(preferred_tags):
                        matching_products.append(product)
            
            if matching_products:
                examples = matching_products[:3]
                result += f'   Examples: {", ".join([p["name"] for p in examples])}\\n'
            
            result += f'   Relevance Score: {score:.2f}\\n'
            result += f'   Store ID: {store["id"]}\\n\\n'
        
        if len(relevant_stores) > limit:
            result += f'... and {len(relevant_stores) - limit} more stores.\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_trending_products(args: Dict[str, Any]) -> List[TextContent]:
    """Get trending products based on various metrics."""
    metric = args.get('metric', 'recent')
    category_filter = args.get('category_filter')
    limit = args.get('limit', 20)
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        # Filter by category if specified
        if category_filter:
            products = [p for p in products if p.get('tags') and 
                       any(tag['name'].lower() == category_filter.lower() for tag in p['tags'])]
        
        if not products:
            return [TextContent(type='text', text=f'No products found{f" in category {category_filter}" if category_filter else ""}.')]
        
        result = f'# 📈 Trending Products{f" - {category_filter}" if category_filter else ""}\\n\\n'
        result += f'**Trending Metric:** {metric.replace("_", " ").title()}\\n'
        result += f'**Products Analyzed:** {len(products)}\\n\\n'
        
        if metric == 'recent':
            # Sort by creation date (most recent first)
            # Note: Using ID as proxy for recency since we don't have created_at in the response
            trending_products = sorted(products, key=lambda x: x['id'], reverse=True)[:limit]
            
            result += '## Recently Added Products\\n\\n'
            for i, product in enumerate(trending_products, 1):
                result += f'{i}. **{product["name"]}**\\n'
                if product.get('price'):
                    result += f'   Price: €{product["price"]}\\n'
                if product.get('store'):
                    result += f'   Store: {product["store"]["name"]}\\n'
                if product.get('tags'):
                    tags = [tag['name'] for tag in product['tags']]
                    result += f'   Categories: {", ".join(tags)}\\n'
                result += f'   ID: {product["id"]}\\n\\n'
        
        elif metric == 'high_value':
            # Sort by price (highest first)
            priced_products = [p for p in products if p.get('price')]
            trending_products = sorted(priced_products, key=lambda x: float(x['price']), reverse=True)[:limit]
            
            result += '## High-Value Products\\n\\n'
            for i, product in enumerate(trending_products, 1):
                result += f'{i}. **{product["name"]}** - €{product["price"]}\\n'
                if product.get('store'):
                    result += f'   Store: {product["store"]["name"]}\\n'
                if product.get('tags'):
                    tags = [tag['name'] for tag in product['tags']]
                    result += f'   Categories: {", ".join(tags)}\\n'
                result += f'   ID: {product["id"]}\\n\\n'
        
        elif metric == 'popular_tags':
            # Find products with most popular tags
            all_tags = []
            for product in products:
                if product.get('tags'):
                    all_tags.extend([tag['name'] for tag in product['tags']])
            
            tag_popularity = Counter(all_tags)
            popular_tags = set(tag for tag, count in tag_popularity.most_common(10))
            
            # Score products by tag popularity
            product_scores = []
            for product in products:
                if product.get('tags'):
                    product_tags = set(tag['name'] for tag in product['tags'])
                    popular_tag_count = len(product_tags.intersection(popular_tags))
                    if popular_tag_count > 0:
                        product_scores.append((product, popular_tag_count))
            
            trending_products = sorted(product_scores, key=lambda x: x[1], reverse=True)[:limit]
            
            result += f'## Products with Popular Categories\\n'
            result += f'**Most Popular Tags:** {", ".join([tag for tag, _ in tag_popularity.most_common(5)])}\\n\\n'
            
            for i, (product, score) in enumerate(trending_products, 1):
                result += f'{i}. **{product["name"]}** ({score} popular categories)\\n'
                if product.get('price'):
                    result += f'   Price: €{product["price"]}\\n'
                if product.get('store'):
                    result += f'   Store: {product["store"]["name"]}\\n'
                popular_product_tags = [tag['name'] for tag in product['tags'] 
                                      if tag['name'] in popular_tags]
                result += f'   Popular Categories: {", ".join(popular_product_tags)}\\n'
                result += f'   ID: {product["id"]}\\n\\n'
        
        elif metric == 'price_gaps':
            # Find products that fill price gaps in their categories
            priced_products = [p for p in products if p.get('price')]
            
            # Group by tags and find price gaps
            gap_products = []
            tag_groups = defaultdict(list)
            
            for product in priced_products:
                if product.get('tags'):
                    for tag in product['tags']:
                        tag_groups[tag['name']].append(product)
            
            for tag, tag_products in tag_groups.items():
                if len(tag_products) >= 3:  # Need enough products to identify gaps
                    prices = sorted([float(p['price']) for p in tag_products])
                    
                    # Find products that are in price gaps
                    for i, product in enumerate(tag_products):
                        product_price = float(product['price'])
                        
                        # Find position in price range
                        position = prices.index(product_price) / (len(prices) - 1) if len(prices) > 1 else 0
                        
                        # Products in middle price ranges (filling gaps) get higher scores
                        if 0.2 <= position <= 0.8:  # Middle 60% of price range
                            gap_score = 1 - abs(position - 0.5) * 2  # Higher score for products closer to median
                            gap_products.append((product, gap_score))
            
            # Remove duplicates and sort
            seen_products = set()
            unique_gap_products = []
            for product, score in gap_products:
                if product['id'] not in seen_products:
                    seen_products.add(product['id'])
                    unique_gap_products.append((product, score))
            
            trending_products = sorted(unique_gap_products, key=lambda x: x[1], reverse=True)[:limit]
            
            result += '## Products Filling Price Gaps\\n\\n'
            for i, (product, score) in enumerate(trending_products, 1):
                result += f'{i}. **{product["name"]}** (gap score: {score:.2f})\\n'
                result += f'   Price: €{product["price"]}\\n'
                if product.get('store'):
                    result += f'   Store: {product["store"]["name"]}\\n'
                if product.get('tags'):
                    tags = [tag['name'] for tag in product['tags']]
                    result += f'   Categories: {", ".join(tags)}\\n'
                result += f'   ID: {product["id"]}\\n\\n'
        
        return [TextContent(type='text', text=result)]


async def _recommend_complementary_products(args: Dict[str, Any]) -> List[TextContent]:
    """Recommend complementary products."""
    product_id = args.get('product_id')
    logic = args.get('complementary_logic', 'different_category')
    limit = args.get('limit', 8)
    
    if not product_id:
        return [TextContent(type='text', text='Error: product_id is required')]
    
    with get_http_client() as client:
        # Get the base product
        target_response = client.get(f'/v1/products/{product_id}')
        if target_response.status_code == 404:
            return [TextContent(type='text', text=f'Product with ID {product_id} not found.')]
        target_response.raise_for_status()
        target_product = target_response.json()
        
        # Get all products
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        result = f'# 🔗 Complementary Products for "{target_product["name"]}"\\n\\n'
        result += f'**Base Product:** {target_product["name"]}\\n'
        if target_product.get('price'):
            result += f'**Base Price:** €{target_product["price"]}\\n'
        result += f'**Complementary Logic:** {logic.replace("_", " ").title()}\\n\\n'
        
        complementary_products = []
        
        if logic == 'different_category':
            # Find products with different categories but potentially related
            target_tags = set()
            if target_product.get('tags'):
                target_tags = set(tag['name'].lower() for tag in target_product['tags'])
            
            for product in products:
                if product['id'] == product_id:
                    continue
                
                if product.get('tags'):
                    product_tags = set(tag['name'].lower() for tag in product['tags'])
                    
                    # Look for products with different but potentially complementary categories
                    if not product_tags.intersection(target_tags) and product_tags:
                        # Score based on some complementary logic (e.g., similar price range)
                        score = 0.5  # Base score for different category
                        
                        # Price similarity bonus (complementary items often in similar price ranges)
                        if target_product.get('price') and product.get('price'):
                            price_ratio = min(float(product['price']), float(target_product['price'])) / max(float(product['price']), float(target_product['price']))
                            if price_ratio > 0.5:  # Similar price range
                                score += 0.3
                        
                        # Store variety bonus
                        if product.get('store_id') != target_product.get('store_id'):
                            score += 0.2
                        
                        complementary_products.append((product, score))
        
        elif logic == 'price_tier':
            # Find products in different price tiers
            target_price = float(target_product['price']) if target_product.get('price') else 0
            
            for product in products:
                if product['id'] == product_id or not product.get('price'):
                    continue
                
                product_price = float(product['price'])
                
                # Define complementary price relationships
                score = 0
                if target_price > 0:
                    ratio = product_price / target_price
                    
                    # Accessories/add-ons (lower price)
                    if 0.1 <= ratio <= 0.5:
                        score = 0.8
                    # Premium upgrades (higher price)
                    elif 1.5 <= ratio <= 3.0:
                        score = 0.6
                    # Similar tier alternatives
                    elif 0.8 <= ratio <= 1.2:
                        score = 0.4
                
                if score > 0:
                    complementary_products.append((product, score))
        
        elif logic == 'store_variety':
            # Find products from different stores
            target_store_id = target_product.get('store_id')
            
            for product in products:
                if (product['id'] == product_id or 
                    product.get('store_id') == target_store_id):
                    continue
                
                score = 0.6  # Base score for different store
                
                # Bonus for similar categories (cross-store shopping)
                if target_product.get('tags') and product.get('tags'):
                    target_tags = set(tag['name'].lower() for tag in target_product['tags'])
                    product_tags = set(tag['name'].lower() for tag in product['tags'])
                    
                    if target_tags.intersection(product_tags):
                        score += 0.3
                
                complementary_products.append((product, score))
        
        # Sort by complementary score
        complementary_products.sort(key=lambda x: x[1], reverse=True)
        
        if not complementary_products:
            result += f'No complementary products found using {logic} logic.\\n'
            result += 'Try a different complementary logic or check if there are enough products in the database.\\n'
            return [TextContent(type='text', text=result)]
        
        result += f'**Complementary Products Found:** {len(complementary_products)}\\n\\n'
        
        # Show recommendations
        for i, (product, score) in enumerate(complementary_products[:limit], 1):
            result += f'{i}. **{product["name"]}** (compatibility: {score:.2f})\\n'
            
            if product.get('price'):
                result += f'   Price: €{product["price"]}'
                if target_product.get('price'):
                    if logic == 'price_tier':
                        ratio = float(product['price']) / float(target_product['price'])
                        if ratio < 0.5:
                            tier = 'Accessory'
                        elif ratio > 1.5:
                            tier = 'Premium upgrade'
                        else:
                            tier = 'Similar tier'
                        result += f' ({tier})'
                result += '\\n'
            
            if product.get('store'):
                result += f'   Store: {product["store"]["name"]}'
                if target_product.get('store'):
                    if product['store']['name'] != target_product['store']['name']:
                        result += ' (different store)'
                result += '\\n'
            
            if product.get('tags'):
                product_tags = [tag['name'] for tag in product['tags']]
                result += f'   Categories: {", ".join(product_tags)}\\n'
            
            # Complementary reasoning
            if logic == 'different_category':
                result += f'   Why complementary: Different product category\\n'
            elif logic == 'price_tier':
                if target_product.get('price') and product.get('price'):
                    ratio = float(product['price']) / float(target_product['price'])
                    if ratio < 0.5:
                        result += f'   Why complementary: Affordable add-on ({ratio:.1f}x price)\\n'
                    elif ratio > 1.5:
                        result += f'   Why complementary: Premium upgrade ({ratio:.1f}x price)\\n'
            elif logic == 'store_variety':
                result += f'   Why complementary: Cross-store shopping opportunity\\n'
            
            result += f'   ID: {product["id"]}\\n\\n'
        
        if len(complementary_products) > limit:
            result += f'... and {len(complementary_products) - limit} more complementary products.\\n'
        
        return [TextContent(type='text', text=result)]


async def _generate_shopping_list(args: Dict[str, Any]) -> List[TextContent]:
    """Generate a curated shopping list."""
    budget = args.get('budget')
    categories = args.get('categories', [])
    store_preference = args.get('store_preference', 'multiple_stores')
    optimization_goal = args.get('optimization_goal', 'best_variety')
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        stores_response = client.get('/v1/stores/')
        
        products_response.raise_for_status()
        stores_response.raise_for_status()
        
        products = products_response.json()
        stores = {s['id']: s for s in stores_response.json()}
        
        # Filter products with prices
        priced_products = [p for p in products if p.get('price')]
        
        result = f'# 🛒 Curated Shopping List\\n\\n'
        result += f'**Parameters:**\\n'
        if budget:
            result += f'  • Budget: €{budget}\\n'
        if categories:
            result += f'  • Required Categories: {", ".join(categories)}\\n'
        result += f'  • Store Preference: {store_preference.replace("_", " ").title()}\\n'
        result += f'  • Optimization Goal: {optimization_goal.replace("_", " ").title()}\\n\\n'
        
        if not priced_products:
            return [TextContent(type='text', text='No products with prices found for shopping list generation.')]
        
        # Apply store filtering
        if store_preference == 'online_only':
            priced_products = [p for p in priced_products if p.get('store') and 
                             stores.get(p.get('store_id'), {}).get('type') == 'online']
        elif store_preference == 'physical_only':
            priced_products = [p for p in priced_products if p.get('store') and 
                             stores.get(p.get('store_id'), {}).get('type') in ['physical', 'chain']]
        
        # Filter by required categories if specified
        if categories:
            category_products = []
            for product in priced_products:
                if product.get('tags'):
                    product_tags = set(tag['name'].lower() for tag in product['tags'])
                    required_tags = set(cat.lower() for cat in categories)
                    if product_tags.intersection(required_tags):
                        category_products.append(product)
            priced_products = category_products
        
        if not priced_products:
            result += 'No products found matching your criteria.\\n'
            return [TextContent(type='text', text=result)]
        
        # Generate shopping list based on optimization goal
        shopping_list = []
        total_cost = 0.0
        
        if optimization_goal == 'lowest_price':
            # Sort by price and add cheapest items
            sorted_products = sorted(priced_products, key=lambda x: float(x['price']))
            
            for product in sorted_products:
                price = float(product['price'])
                if not budget or total_cost + price <= budget:
                    shopping_list.append(product)
                    total_cost += price
                    
                    if budget and total_cost >= budget * 0.95:  # Stop at 95% of budget
                        break
        
        elif optimization_goal == 'best_variety':
            # Try to get products from different categories and stores
            added_categories = set()
            added_stores = set()
            
            # Prioritize products that add new categories or stores
            product_scores = []
            for product in priced_products:
                score = 0
                
                # Category variety bonus
                if product.get('tags'):
                    product_tags = set(tag['name'].lower() for tag in product['tags'])
                    new_categories = product_tags - added_categories
                    score += len(new_categories) * 2
                
                # Store variety bonus
                if product.get('store_id') and product['store_id'] not in added_stores:
                    score += 1
                
                # Price consideration (prefer mid-range)
                price = float(product['price'])
                if budget:
                    price_ratio = price / (budget / 10)  # Assume 10 items average
                    if 0.5 <= price_ratio <= 2.0:  # Reasonable price range
                        score += 0.5
                
                product_scores.append((product, score))
            
            # Sort by variety score
            product_scores.sort(key=lambda x: x[1], reverse=True)
            
            for product, score in product_scores:
                price = float(product['price'])
                if not budget or total_cost + price <= budget:
                    shopping_list.append(product)
                    total_cost += price
                    
                    # Update variety tracking
                    if product.get('tags'):
                        product_tags = set(tag['name'].lower() for tag in product['tags'])
                        added_categories.update(product_tags)
                    
                    if product.get('store_id'):
                        added_stores.add(product['store_id'])
                    
                    if budget and total_cost >= budget * 0.95:
                        break
        
        elif optimization_goal == 'convenience':
            # Minimize number of stores
            if store_preference == 'single_store':
                # Find the store with most matching products
                store_product_counts = defaultdict(list)
                for product in priced_products:
                    if product.get('store_id'):
                        store_product_counts[product['store_id']].append(product)
                
                if store_product_counts:
                    best_store_id = max(store_product_counts.keys(), 
                                      key=lambda x: len(store_product_counts[x]))
                    store_products = store_product_counts[best_store_id]
                    
                    # Sort by price for budget optimization
                    store_products.sort(key=lambda x: float(x['price']))
                    
                    for product in store_products:
                        price = float(product['price'])
                        if not budget or total_cost + price <= budget:
                            shopping_list.append(product)
                            total_cost += price
                            
                            if budget and total_cost >= budget * 0.95:
                                break
            else:
                # Prefer products from fewer stores
                store_priorities = Counter(p.get('store_id') for p in priced_products if p.get('store_id'))
                
                def convenience_score(product):
                    store_id = product.get('store_id')
                    store_popularity = store_priorities.get(store_id, 0)
                    price = float(product['price'])
                    return store_popularity / price  # Higher score for popular stores with lower prices
                
                sorted_products = sorted(priced_products, key=convenience_score, reverse=True)
                
                for product in sorted_products:
                    price = float(product['price'])
                    if not budget or total_cost + price <= budget:
                        shopping_list.append(product)
                        total_cost += price
                        
                        if budget and total_cost >= budget * 0.95:
                            break
        
        # Display shopping list
        if not shopping_list:
            result += 'Could not generate a shopping list with the specified constraints.\\n'
            return [TextContent(type='text', text=result)]
        
        result += f'## Generated Shopping List ({len(shopping_list)} items)\\n\\n'
        
        # Group by store for convenience
        store_groups = defaultdict(list)
        for product in shopping_list:
            store_id = product.get('store_id', 'unknown')
            store_groups[store_id].append(product)
        
        for store_id, store_products in store_groups.items():
            if store_id != 'unknown' and store_id in stores:
                store_name = stores[store_id]['name']
                store_type = stores[store_id].get('type', 'unknown')
                result += f'### {store_name} ({store_type}) - {len(store_products)} items\\n'
            else:
                result += f'### Unknown Store - {len(store_products)} items\\n'
            
            store_total = sum(float(p['price']) for p in store_products)
            result += f'**Store Total: €{store_total:.2f}**\\n\\n'
            
            for product in store_products:
                result += f'• **{product["name"]}** - €{product["price"]}\\n'
                if product.get('tags'):
                    tags = [tag['name'] for tag in product['tags']]
                    result += f'  Categories: {", ".join(tags)}\\n'
                result += f'  ID: {product["id"]}\\n\\n'
        
        # Summary
        result += f'## Shopping Summary\\n'
        result += f'**Total Cost:** €{total_cost:.2f}\\n'
        if budget:
            remaining = budget - total_cost
            result += f'**Budget Used:** {total_cost/budget*100:.1f}% (€{remaining:.2f} remaining)\\n'
        
        result += f'**Number of Stores:** {len(store_groups)}\\n'
        result += f'**Number of Items:** {len(shopping_list)}\\n'
        
        # Category coverage
        all_categories = set()
        for product in shopping_list:
            if product.get('tags'):
                all_categories.update(tag['name'] for tag in product['tags'])
        
        result += f'**Categories Covered:** {len(all_categories)}\\n'
        if all_categories:
            result += f'**Categories:** {", ".join(sorted(all_categories))}\\n'
        
        return [TextContent(type='text', text=result)]


async def _recommend_price_alerts(args: Dict[str, Any]) -> List[TextContent]:
    """Recommend price alerts to set up."""
    categories = args.get('categories', [])
    alert_type = args.get('alert_type', 'price_drops')
    limit = args.get('limit', 15)
    
    with get_http_client() as client:
        products_response = client.get('/v1/products/', params={'limit': 1000})
        products_response.raise_for_status()
        products = products_response.json()
        
        # Filter by categories if specified
        if categories:
            filtered_products = []
            for product in products:
                if product.get('tags'):
                    product_tags = set(tag['name'].lower() for tag in product['tags'])
                    category_tags = set(cat.lower() for cat in categories)
                    if product_tags.intersection(category_tags):
                        filtered_products.append(product)
            products = filtered_products
        
        priced_products = [p for p in products if p.get('price')]
        
        result = f'# 🔔 Price Alert Recommendations\\n\\n'
        result += f'**Alert Type:** {alert_type.replace("_", " ").title()}\\n'
        if categories:
            result += f'**Categories:** {", ".join(categories)}\\n'
        result += f'**Products Analyzed:** {len(priced_products)}\\n\\n'
        
        if not priced_products:
            result += 'No priced products found for alert recommendations.\\n'
            return [TextContent(type='text', text=result)]
        
        alert_recommendations = []
        
        if alert_type == 'overpriced':
            # Find products that are significantly more expensive than similar items
            for product in priced_products:
                if not product.get('tags'):
                    continue
                
                # Find similar products by tags
                product_tags = set(tag['name'].lower() for tag in product['tags'])
                similar_products = []
                
                for other_product in priced_products:
                    if (other_product['id'] != product['id'] and 
                        other_product.get('tags')):
                        other_tags = set(tag['name'].lower() for tag in other_product['tags'])
                        if product_tags.intersection(other_tags):
                            similar_products.append(other_product)
                
                if len(similar_products) >= 2:
                    similar_prices = [float(p['price']) for p in similar_products]
                    avg_similar_price = sum(similar_prices) / len(similar_prices)
                    product_price = float(product['price'])
                    
                    if product_price > avg_similar_price * 1.3:  # 30% more expensive
                        overpriced_factor = product_price / avg_similar_price
                        alert_recommendations.append((product, overpriced_factor, 'overpriced'))
        
        elif alert_type == 'underpriced':
            # Find products that are significantly cheaper than similar items
            for product in priced_products:
                if not product.get('tags'):
                    continue
                
                product_tags = set(tag['name'].lower() for tag in product['tags'])
                similar_products = []
                
                for other_product in priced_products:
                    if (other_product['id'] != product['id'] and 
                        other_product.get('tags')):
                        other_tags = set(tag['name'].lower() for tag in other_product['tags'])
                        if product_tags.intersection(other_tags):
                            similar_products.append(other_product)
                
                if len(similar_products) >= 2:
                    similar_prices = [float(p['price']) for p in similar_products]
                    avg_similar_price = sum(similar_prices) / len(similar_prices)
                    product_price = float(product['price'])
                    
                    if product_price < avg_similar_price * 0.7:  # 30% cheaper
                        underpriced_factor = avg_similar_price / product_price
                        alert_recommendations.append((product, underpriced_factor, 'underpriced'))
        
        elif alert_type == 'price_drops':
            # Recommend high-value products that might have price drops
            high_value_products = [p for p in priced_products if float(p['price']) > 50]
            
            # Prioritize products with competitive markets (multiple similar products)
            for product in high_value_products:
                if not product.get('tags'):
                    continue
                
                product_tags = set(tag['name'].lower() for tag in product['tags'])
                similar_count = 0
                
                for other_product in priced_products:
                    if (other_product['id'] != product['id'] and 
                        other_product.get('tags')):
                        other_tags = set(tag['name'].lower() for tag in other_product['tags'])
                        if product_tags.intersection(other_tags):
                            similar_count += 1
                
                if similar_count >= 2:  # Competitive market
                    price = float(product['price'])
                    # Score based on price (higher price = more potential for drops) and competition
                    drop_potential = math.log(price) * similar_count
                    alert_recommendations.append((product, drop_potential, 'price_drop'))
        
        elif alert_type == 'new_products':
            # Recommend setting alerts for new products in categories of interest
            # Use product ID as proxy for recency
            recent_products = sorted(priced_products, key=lambda x: x['id'], reverse=True)
            
            for product in recent_products[:limit]:
                newness_score = product['id']  # Higher ID = more recent
                alert_recommendations.append((product, newness_score, 'new_product'))
        
        # Sort recommendations by score
        alert_recommendations.sort(key=lambda x: x[1], reverse=True)
        
        if not alert_recommendations:
            result += f'No {alert_type.replace("_", " ")} alert opportunities found.\\n'
            result += 'Try different categories or alert types.\\n'
            return [TextContent(type='text', text=result)]
        
        result += f'## Top {alert_type.replace("_", " ").title()} Alert Recommendations\\n\\n'
        
        for i, (product, score, alert_reason) in enumerate(alert_recommendations[:limit], 1):
            result += f'{i}. **{product["name"]}**\\n'
            result += f'   Current Price: €{product["price"]}\\n'
            
            if product.get('store'):
                result += f'   Store: {product["store"]["name"]}\\n'
            
            if product.get('tags'):
                tags = [tag['name'] for tag in product['tags']]
                result += f'   Categories: {", ".join(tags)}\\n'
            
            # Alert reasoning
            if alert_reason == 'overpriced':
                result += f'   Alert Reason: {score:.1f}x more expensive than similar products\\n'
                result += f'   Expected: Price may drop due to competition\\n'
            elif alert_reason == 'underpriced':
                result += f'   Alert Reason: {score:.1f}x cheaper than similar products\\n'
                result += f'   Expected: Price may increase (good deal now)\\n'
            elif alert_reason == 'price_drop':
                result += f'   Alert Reason: High-value product in competitive market\\n'
                result += f'   Expected: Potential for discounts/sales\\n'
            elif alert_reason == 'new_product':
                result += f'   Alert Reason: Recently added product\\n'
                result += f'   Expected: Price may stabilize or drop after launch\\n'
            
            result += f'   Product ID: {product["id"]}\\n\\n'
        
        if len(alert_recommendations) > limit:
            result += f'... and {len(alert_recommendations) - limit} more alert opportunities.\\n'
        
        # Setup instructions
        result += '\\n## How to Use These Recommendations\\n'
        result += '1. **Monitor prices** of the recommended products regularly\\n'
        result += '2. **Set price thresholds** based on the analysis provided\\n'
        result += '3. **Track market trends** in the categories you are interested in\\n'
        result += '4. **Compare prices** across different stores before purchasing\\n'
        
        return [TextContent(type='text', text=result)]


if __name__ == '__main__':
    # This will be called by the run script
    logger.info('Starting Partle Recommendations MCP Server')
    mcp_server.run()
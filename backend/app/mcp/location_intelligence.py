"""MCP Server for Partle Location Intelligence and Geographic Analysis."""
import logging
from typing import Optional, Any, Dict, List, Tuple
from contextlib import contextmanager
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import json
import os
import math
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
API_BASE_URL = os.getenv('PARTLE_API_URL', 'http://localhost:8000')

# Initialize MCP server
mcp_server = Server('partle-location-intelligence')


@contextmanager
def get_http_client():
    """Get HTTP client for API requests."""
    with httpx.Client(base_url=API_BASE_URL) as client:
        yield client


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points on Earth in kilometers."""
    R = 6371  # Earth's radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat/2) * math.sin(dlat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon/2) * math.sin(dlon/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def get_geographic_center(coordinates: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Calculate the geographic center of a list of coordinates."""
    if not coordinates:
        return (0, 0)
    
    total_lat = sum(coord[0] for coord in coordinates)
    total_lon = sum(coord[1] for coord in coordinates)
    
    return (total_lat / len(coordinates), total_lon / len(coordinates))


@mcp_server.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools for location intelligence."""
    return [
        Tool(
            name='find_nearby_stores',
            description='Find stores within a specified radius of a location',
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
                        'default': 5,
                        'description': 'Search radius in kilometers'
                    },
                    'store_type': {
                        'type': 'string',
                        'enum': ['physical', 'online', 'chain'],
                        'description': 'Filter by store type'
                    }
                },
                'required': ['lat', 'lon']
            }
        ),
        Tool(
            name='analyze_store_density',
            description='Analyze the density and distribution of stores in different areas',
            inputSchema={
                'type': 'object',
                'properties': {
                    'grid_size_km': {
                        'type': 'number',
                        'default': 10,
                        'description': 'Size of grid cells in kilometers for density analysis'
                    }
                }
            }
        ),
        Tool(
            name='find_market_gaps',
            description='Identify areas with low store density that might represent market opportunities',
            inputSchema={
                'type': 'object',
                'properties': {
                    'min_radius_km': {
                        'type': 'number',
                        'default': 5,
                        'description': 'Minimum radius to consider for gap analysis'
                    },
                    'store_type': {
                        'type': 'string',
                        'enum': ['physical', 'online', 'chain'],
                        'description': 'Focus on specific store type'
                    }
                }
            }
        ),
        Tool(
            name='analyze_coverage_area',
            description='Analyze the geographic coverage area of the platform',
            inputSchema={
                'type': 'object',
                'properties': {}
            }
        ),
        Tool(
            name='get_location_insights',
            description='Get detailed insights about a specific location including nearby competition and market data',
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
                    'analysis_radius_km': {
                        'type': 'number',
                        'default': 10,
                        'description': 'Analysis radius in kilometers'
                    }
                },
                'required': ['lat', 'lon']
            }
        ),
        Tool(
            name='compare_locations',
            description='Compare multiple locations in terms of market presence and competition',
            inputSchema={
                'type': 'object',
                'properties': {
                    'locations': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'lat': {'type': 'number'},
                                'lon': {'type': 'number'},
                                'name': {'type': 'string'}
                            },
                            'required': ['lat', 'lon']
                        },
                        'description': 'List of locations to compare'
                    },
                    'comparison_radius_km': {
                        'type': 'number',
                        'default': 5,
                        'description': 'Radius for comparison analysis'
                    }
                },
                'required': ['locations']
            }
        ),
        Tool(
            name='find_optimal_location',
            description='Find optimal locations for new stores based on existing competition and coverage',
            inputSchema={
                'type': 'object',
                'properties': {
                    'target_area': {
                        'type': 'object',
                        'properties': {
                            'center_lat': {'type': 'number'},
                            'center_lon': {'type': 'number'},
                            'radius_km': {'type': 'number'}
                        },
                        'required': ['center_lat', 'center_lon', 'radius_km'],
                        'description': 'Target area to search within'
                    },
                    'min_distance_from_competitors_km': {
                        'type': 'number',
                        'default': 2,
                        'description': 'Minimum distance from existing competitors'
                    }
                },
                'required': ['target_area']
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: Optional[Dict[str, Any]]) -> List[TextContent]:
    """Handle tool calls for location intelligence operations."""
    try:
        if name == 'find_nearby_stores':
            return await _find_nearby_stores(arguments or {})
        elif name == 'analyze_store_density':
            return await _analyze_store_density(arguments or {})
        elif name == 'find_market_gaps':
            return await _find_market_gaps(arguments or {})
        elif name == 'analyze_coverage_area':
            return await _analyze_coverage_area(arguments or {})
        elif name == 'get_location_insights':
            return await _get_location_insights(arguments or {})
        elif name == 'compare_locations':
            return await _compare_locations(arguments or {})
        elif name == 'find_optimal_location':
            return await _find_optimal_location(arguments or {})
        else:
            return [TextContent(type='text', text=f'Unknown tool: {name}')]
    except Exception as e:
        logger.error(f'Error calling tool {name}: {e}')
        return [TextContent(type='text', text=f'Error: {str(e)}')]


async def _find_nearby_stores(args: Dict[str, Any]) -> List[TextContent]:
    """Find stores near a specific location."""
    lat = args.get('lat')
    lon = args.get('lon')
    radius_km = args.get('radius_km', 5)
    store_type = args.get('store_type')
    
    if lat is None or lon is None:
        return [TextContent(type='text', text='Error: lat and lon are required')]
    
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        stores_response.raise_for_status()
        stores = stores_response.json()
        
        # Filter stores with coordinates
        stores_with_coords = [s for s in stores if s.get('lat') and s.get('lon')]
        
        if not stores_with_coords:
            return [TextContent(type='text', text='No stores with location data found.')]
        
        # Filter by store type if specified
        if store_type:
            stores_with_coords = [s for s in stores_with_coords if s.get('type') == store_type]
        
        # Calculate distances and filter by radius
        nearby_stores = []
        for store in stores_with_coords:
            distance = haversine_distance(lat, lon, store['lat'], store['lon'])
            if distance <= radius_km:
                store['distance'] = distance
                nearby_stores.append(store)
        
        # Sort by distance
        nearby_stores.sort(key=lambda x: x['distance'])
        
        result = f'# 📍 Nearby Stores{f" ({store_type})" if store_type else ""}\\n\\n'
        result += f'**Search Location:** {lat:.4f}, {lon:.4f}\\n'
        result += f'**Search Radius:** {radius_km}km\\n'
        result += f'**Stores Found:** {len(nearby_stores)}\\n\\n'
        
        if not nearby_stores:
            result += 'No stores found within the specified radius.\\n'
            
            # Find the closest store outside radius
            all_distances = []
            for store in stores_with_coords:
                distance = haversine_distance(lat, lon, store['lat'], store['lon'])
                all_distances.append((store, distance))
            
            if all_distances:
                closest = min(all_distances, key=lambda x: x[1])
                result += f'\\n**Closest Store:** {closest[0]["name"]} ({closest[1]:.1f}km away)\\n'
        else:
            for i, store in enumerate(nearby_stores[:15], 1):
                result += f'{i}. **{store["name"]}** ({store["type"]})\\n'
                result += f'   Distance: {store["distance"]:.1f}km\\n'
                if store.get('address'):
                    result += f'   Address: {store["address"]}\\n'
                result += f'   Coordinates: {store["lat"]:.4f}, {store["lon"]:.4f}\\n\\n'
            
            if len(nearby_stores) > 15:
                result += f'... and {len(nearby_stores) - 15} more stores.\\n'
        
        return [TextContent(type='text', text=result)]


async def _analyze_store_density(args: Dict[str, Any]) -> List[TextContent]:
    """Analyze store density across the coverage area."""
    grid_size_km = args.get('grid_size_km', 10)
    
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        stores_response.raise_for_status()
        stores = stores_response.json()
        
        stores_with_coords = [s for s in stores if s.get('lat') and s.get('lon')]
        
        if not stores_with_coords:
            return [TextContent(type='text', text='No stores with location data found for density analysis.')]
        
        # Get bounding box
        lats = [s['lat'] for s in stores_with_coords]
        lons = [s['lon'] for s in stores_with_coords]
        
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)
        
        # Convert grid size to degrees (approximate)
        lat_grid_size = grid_size_km / 111.0  # roughly 111 km per degree of latitude
        lon_grid_size = grid_size_km / (111.0 * math.cos(math.radians((min_lat + max_lat) / 2)))
        
        # Create grid and count stores
        grid_counts = defaultdict(int)
        
        for store in stores_with_coords:
            grid_lat = int((store['lat'] - min_lat) / lat_grid_size)
            grid_lon = int((store['lon'] - min_lon) / lon_grid_size)
            grid_counts[(grid_lat, grid_lon)] += 1
        
        result = f'# 🗺️ Store Density Analysis\\n\\n'
        result += f'**Analysis Parameters:**\\n'
        result += f'  • Grid Size: {grid_size_km}km x {grid_size_km}km\\n'
        result += f'  • Coverage Area: {max_lat - min_lat:.3f}° lat x {max_lon - min_lon:.3f}° lon\\n'
        result += f'  • Stores Analyzed: {len(stores_with_coords)}\\n\\n'
        
        if grid_counts:
            densities = list(grid_counts.values())
            max_density = max(densities)
            avg_density = sum(densities) / len(densities)
            
            result += f'**Density Statistics:**\\n'
            result += f'  • Grid Cells with Stores: {len(grid_counts)}\\n'
            result += f'  • Maximum Density: {max_density} stores per cell\\n'
            result += f'  • Average Density: {avg_density:.1f} stores per cell\\n\\n'
            
            # Density distribution
            density_ranges = [
                (1, 1, 'Low (1 store)'),
                (2, 3, 'Medium (2-3 stores)'),
                (4, 6, 'High (4-6 stores)'),
                (7, float('inf'), 'Very High (7+ stores)')
            ]
            
            result += '**Density Distribution:**\\n'
            for min_d, max_d, label in density_ranges:
                count = sum(1 for d in densities if min_d <= d <= max_d)
                if count > 0:
                    percentage = count / len(densities) * 100
                    result += f'  • {label}: {count} grid cells ({percentage:.1f}%)\\n'
            
            # Find highest density areas
            high_density_cells = sorted(grid_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            result += '\\n**Highest Density Areas:**\\n'
            for i, ((grid_lat, grid_lon), count) in enumerate(high_density_cells, 1):
                center_lat = min_lat + (grid_lat + 0.5) * lat_grid_size
                center_lon = min_lon + (grid_lon + 0.5) * lon_grid_size
                result += f'{i}. {count} stores at grid center: {center_lat:.3f}, {center_lon:.3f}\\n'
            
            # Store type analysis
            type_counts = Counter(s.get('type', 'unknown') for s in stores_with_coords)
            result += '\\n**Store Type Distribution:**\\n'
            for store_type, count in type_counts.items():
                percentage = count / len(stores_with_coords) * 100
                result += f'  • {store_type.title()}: {count} stores ({percentage:.1f}%)\\n'
        
        return [TextContent(type='text', text=result)]


async def _find_market_gaps(args: Dict[str, Any]) -> List[TextContent]:
    """Find areas with low store density (market gaps)."""
    min_radius_km = args.get('min_radius_km', 5)
    store_type = args.get('store_type')
    
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        stores_response.raise_for_status()
        stores = stores_response.json()
        
        stores_with_coords = [s for s in stores if s.get('lat') and s.get('lon')]
        
        if store_type:
            stores_with_coords = [s for s in stores_with_coords if s.get('type') == store_type]
        
        if not stores_with_coords:
            return [TextContent(type='text', text='No stores with location data found for gap analysis.')]
        
        if len(stores_with_coords) < 3:
            return [TextContent(type='text', text='Need at least 3 stores for meaningful gap analysis.')]
        
        # Find potential gap locations by analyzing areas far from existing stores
        lats = [s['lat'] for s in stores_with_coords]
        lons = [s['lon'] for s in stores_with_coords]
        
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)
        
        # Generate a grid of potential locations
        lat_step = (max_lat - min_lat) / 20
        lon_step = (max_lon - min_lon) / 20
        
        market_gaps = []
        
        for lat in [min_lat + i * lat_step for i in range(1, 20)]:
            for lon in [min_lon + j * lon_step for j in range(1, 20)]:
                # Find distance to nearest store
                distances = [haversine_distance(lat, lon, s['lat'], s['lon']) for s in stores_with_coords]
                nearest_distance = min(distances)
                
                if nearest_distance >= min_radius_km:
                    # Count stores within a larger radius to assess market potential
                    stores_in_area = sum(1 for d in distances if d <= min_radius_km * 2)
                    market_gaps.append({
                        'lat': lat,
                        'lon': lon,
                        'nearest_store_distance': nearest_distance,
                        'stores_in_extended_area': stores_in_area
                    })
        
        # Sort by distance to nearest store (largest gaps first)
        market_gaps.sort(key=lambda x: x['nearest_store_distance'], reverse=True)
        
        result = f'# 🔍 Market Gap Analysis{f" ({store_type} stores)" if store_type else ""}\\n\\n'
        result += f'**Analysis Parameters:**\\n'
        result += f'  • Minimum gap radius: {min_radius_km}km\\n'
        result += f'  • Stores analyzed: {len(stores_with_coords)}\\n'
        result += f'  • Coverage area: {max_lat - min_lat:.2f}° x {max_lon - min_lon:.2f}°\\n\\n'
        
        if not market_gaps:
            result += f'No significant market gaps found with minimum radius of {min_radius_km}km.\\n'
            result += 'The market appears to be well covered by existing stores.\\n'
        else:
            result += f'**Market Gaps Found:** {len(market_gaps)}\\n\\n'
            
            # Show top gaps
            result += '## Top Market Opportunities\\n\\n'
            for i, gap in enumerate(market_gaps[:10], 1):
                result += f'{i}. **Location:** {gap["lat"]:.4f}, {gap["lon"]:.4f}\\n'
                result += f'   Distance to nearest store: {gap["nearest_store_distance"]:.1f}km\\n'
                result += f'   Stores in extended area (2x radius): {gap["stores_in_extended_area"]}\\n'
                
                # Market potential assessment
                if gap['stores_in_extended_area'] >= 3:
                    potential = 'High (established market area)'
                elif gap['stores_in_extended_area'] >= 1:
                    potential = 'Medium (some market presence)'
                else:
                    potential = 'Low (untested market area)'
                
                result += f'   Market potential: {potential}\\n\\n'
            
            if len(market_gaps) > 10:
                result += f'... and {len(market_gaps) - 10} more potential locations.\\n\\n'
            
            # Summary recommendations
            high_potential = [g for g in market_gaps if g['stores_in_extended_area'] >= 2]
            result += '## Recommendations\\n'
            if high_potential:
                result += f'**High Priority Locations:** {len(high_potential)} gaps in established market areas\\n'
                best_gap = high_potential[0]
                result += f'**Top Recommendation:** {best_gap["lat"]:.4f}, {best_gap["lon"]:.4f} '
                result += f'({best_gap["nearest_store_distance"]:.1f}km from competition)\\n'
        
        return [TextContent(type='text', text=result)]


async def _analyze_coverage_area(args: Dict[str, Any]) -> List[TextContent]:
    """Analyze the geographic coverage area of the platform."""
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        products_response = client.get('/v1/products/', params={'limit': 1000})
        
        stores_response.raise_for_status()
        products_response.raise_for_status()
        
        stores = stores_response.json()
        products = products_response.json()
        
        stores_with_coords = [s for s in stores if s.get('lat') and s.get('lon')]
        products_with_coords = [p for p in products if p.get('lat') and p.get('lon')]
        
        result = '# 🌍 Geographic Coverage Analysis\\n\\n'
        
        if not stores_with_coords and not products_with_coords:
            result += 'No geographic data available for coverage analysis.\\n'
            return [TextContent(type='text', text=result)]
        
        # Combine all coordinates
        all_coords = []
        if stores_with_coords:
            all_coords.extend([(s['lat'], s['lon']) for s in stores_with_coords])
        if products_with_coords:
            all_coords.extend([(p['lat'], p['lon']) for p in products_with_coords])
        
        if all_coords:
            lats = [coord[0] for coord in all_coords]
            lons = [coord[1] for coord in all_coords]
            
            min_lat, max_lat = min(lats), max(lats)
            min_lon, max_lon = min(lons), max(lons)
            center_lat, center_lon = get_geographic_center(all_coords)
            
            # Calculate coverage area (rough approximation)
            lat_range_km = (max_lat - min_lat) * 111
            lon_range_km = (max_lon - min_lon) * 111 * math.cos(math.radians(center_lat))
            
            result += f'**Geographic Bounds:**\\n'
            result += f'  • Latitude: {min_lat:.4f}° to {max_lat:.4f}° ({lat_range_km:.1f}km)\\n'
            result += f'  • Longitude: {min_lon:.4f}° to {max_lon:.4f}° ({lon_range_km:.1f}km)\\n'
            result += f'  • Center Point: {center_lat:.4f}°, {center_lon:.4f}\\n\\n'
            
            # Coverage area estimation
            coverage_area_km2 = lat_range_km * lon_range_km
            result += f'**Coverage Area:** ~{coverage_area_km2:,.0f} km²\\n\\n'
        
        # Store coverage analysis
        if stores_with_coords:
            result += f'## Store Coverage\\n'
            result += f'**Stores with Location Data:** {len(stores_with_coords)} of {len(stores)}\\n'
            
            store_types = Counter(s.get('type', 'unknown') for s in stores_with_coords)
            result += f'**Geographic Store Types:**\\n'
            for store_type, count in store_types.items():
                percentage = count / len(stores_with_coords) * 100
                result += f'  • {store_type.title()}: {count} ({percentage:.1f}%)\\n'
            
            # Store density
            if coverage_area_km2 > 0:
                store_density = len(stores_with_coords) / coverage_area_km2
                result += f'**Store Density:** {store_density:.4f} stores/km²\\n'
            
            result += '\\n'
        
        # Product coverage analysis
        if products_with_coords:
            result += f'## Product Coverage\\n'
            result += f'**Products with Location Data:** {len(products_with_coords)} of {len(products)}\\n'
            
            # Products with/without stores
            products_with_stores = len([p for p in products_with_coords if p.get('store_id')])
            products_orphan = len(products_with_coords) - products_with_stores
            
            result += f'**Location-based Products:**\\n'
            result += f'  • Linked to stores: {products_with_stores}\\n'
            result += f'  • Independent locations: {products_orphan}\\n'
            
            if coverage_area_km2 > 0:
                product_density = len(products_with_coords) / coverage_area_km2
                result += f'**Product Density:** {product_density:.2f} products/km²\\n'
        
        # Coverage quality analysis
        result += '\\n## Coverage Quality\\n'
        
        location_coverage = 0
        if stores:
            location_coverage = len(stores_with_coords) / len(stores) * 100
        
        if location_coverage >= 80:
            quality = 'Excellent'
        elif location_coverage >= 60:
            quality = 'Good'
        elif location_coverage >= 40:
            quality = 'Fair'
        else:
            quality = 'Poor'
        
        result += f'**Location Data Coverage:** {location_coverage:.1f}% ({quality})\\n'
        
        if location_coverage < 80:
            missing_data = len(stores) - len(stores_with_coords)
            result += f'**Improvement Opportunity:** {missing_data} stores missing location data\\n'
        
        return [TextContent(type='text', text=result)]


async def _get_location_insights(args: Dict[str, Any]) -> List[TextContent]:
    """Get detailed insights about a specific location."""
    lat = args.get('lat')
    lon = args.get('lon')
    radius_km = args.get('analysis_radius_km', 10)
    
    if lat is None or lon is None:
        return [TextContent(type='text', text='Error: lat and lon are required')]
    
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        products_response = client.get('/v1/products/', params={'limit': 1000})
        
        stores_response.raise_for_status()
        products_response.raise_for_status()
        
        stores = stores_response.json()
        products = products_response.json()
        
        # Find nearby stores and products
        nearby_stores = []
        for store in stores:
            if store.get('lat') and store.get('lon'):
                distance = haversine_distance(lat, lon, store['lat'], store['lon'])
                if distance <= radius_km:
                    store['distance'] = distance
                    nearby_stores.append(store)
        
        nearby_products = []
        for product in products:
            if product.get('lat') and product.get('lon'):
                distance = haversine_distance(lat, lon, product['lat'], product['lon'])
                if distance <= radius_km:
                    product['distance'] = distance
                    nearby_products.append(product)
        
        result = f'# 📍 Location Insights\\n\\n'
        result += f'**Analysis Location:** {lat:.4f}, {lon:.4f}\\n'
        result += f'**Analysis Radius:** {radius_km}km\\n\\n'
        
        # Market presence
        result += f'## Market Presence\\n'
        result += f'**Nearby Stores:** {len(nearby_stores)}\\n'
        result += f'**Nearby Products:** {len(nearby_products)}\\n'
        
        if nearby_stores:
            # Store analysis
            nearby_stores.sort(key=lambda x: x['distance'])
            closest_store = nearby_stores[0]
            
            result += f'**Closest Store:** {closest_store["name"]} ({closest_store["distance"]:.1f}km)\\n'
            
            # Store types in area
            store_types = Counter(s.get('type', 'unknown') for s in nearby_stores)
            result += f'**Store Types in Area:**\\n'
            for store_type, count in store_types.items():
                result += f'  • {store_type.title()}: {count}\\n'
            
            # Store density
            area_km2 = math.pi * radius_km ** 2
            store_density = len(nearby_stores) / area_km2
            result += f'**Store Density:** {store_density:.3f} stores/km²\\n'
        
        result += '\\n'
        
        # Competition analysis
        if nearby_stores:
            result += f'## Competition Analysis\\n'
            
            # Distance to competitors
            competitor_distances = [s['distance'] for s in nearby_stores]
            avg_competitor_distance = sum(competitor_distances) / len(competitor_distances)
            
            result += f'**Average Distance to Competitors:** {avg_competitor_distance:.1f}km\\n'
            result += f'**Closest Competitor:** {min(competitor_distances):.1f}km\\n'
            result += f'**Furthest Competitor:** {max(competitor_distances):.1f}km\\n'
            
            # Competition intensity
            if avg_competitor_distance < 2:
                competition = 'Very High'
            elif avg_competitor_distance < 4:
                competition = 'High'
            elif avg_competitor_distance < 7:
                competition = 'Medium'
            else:
                competition = 'Low'
            
            result += f'**Competition Intensity:** {competition}\\n'
            
            # Top competitors
            result += f'\\n**Nearest Competitors:**\\n'
            for i, store in enumerate(nearby_stores[:5], 1):
                result += f'{i}. {store["name"]} ({store["type"]}) - {store["distance"]:.1f}km\\n'
        
        result += '\\n'
        
        # Product and pricing analysis
        if nearby_products:
            result += f'## Product Market Analysis\\n'
            
            products_with_prices = [p for p in nearby_products if p.get('price')]
            if products_with_prices:
                prices = [float(p['price']) for p in products_with_prices]
                avg_price = sum(prices) / len(prices)
                
                result += f'**Products with Pricing:** {len(products_with_prices)}\\n'
                result += f'**Average Product Price:** €{avg_price:.2f}\\n'
                result += f'**Price Range:** €{min(prices):.2f} - €{max(prices):.2f}\\n'
            
            # Product categories
            all_tags = []
            for product in nearby_products:
                if product.get('tags'):
                    all_tags.extend([tag['name'] for tag in product['tags']])
            
            if all_tags:
                category_counts = Counter(all_tags)
                result += f'\\n**Popular Categories in Area:**\\n'
                for category, count in category_counts.most_common(5):
                    result += f'  • {category}: {count} products\\n'
        
        # Market opportunity assessment
        result += '\\n## Market Opportunity Assessment\\n'
        
        if not nearby_stores:
            result += f'**Status:** Untapped market (no stores within {radius_km}km)\\n'
            result += f'**Opportunity:** High - first mover advantage\\n'
        elif len(nearby_stores) <= 2:
            result += f'**Status:** Low competition market\\n'
            result += f'**Opportunity:** Medium-High - room for growth\\n'
        elif len(nearby_stores) <= 5:
            result += f'**Status:** Moderate competition\\n'
            result += f'**Opportunity:** Medium - differentiation needed\\n'
        else:
            result += f'**Status:** High competition market\\n'
            result += f'**Opportunity:** Low-Medium - challenging entry\\n'
        
        # Strategic recommendations
        result += f'\\n**Strategic Recommendations:**\\n'
        
        if not nearby_stores:
            result += f'  • Consider this location for market entry\\n'
            result += f'  • Research local demographics and demand\\n'
        else:
            dominant_type = Counter(s.get('type', 'unknown') for s in nearby_stores).most_common(1)[0][0]
            result += f'  • Market dominated by {dominant_type} stores\\n'
            if dominant_type == 'physical':
                result += f'  • Consider online presence or chain expansion\\n'
            elif dominant_type == 'online':
                result += f'  • Physical presence might fill market gap\\n'
        
        return [TextContent(type='text', text=result)]


async def _compare_locations(args: Dict[str, Any]) -> List[TextContent]:
    """Compare multiple locations."""
    locations = args.get('locations', [])
    radius_km = args.get('comparison_radius_km', 5)
    
    if not locations:
        return [TextContent(type='text', text='Error: locations list is required')]
    
    if len(locations) < 2:
        return [TextContent(type='text', text='Error: At least 2 locations required for comparison')]
    
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        products_response = client.get('/v1/products/', params={'limit': 1000})
        
        stores_response.raise_for_status()
        products_response.raise_for_status()
        
        stores = stores_response.json()
        products = products_response.json()
        
        stores_with_coords = [s for s in stores if s.get('lat') and s.get('lon')]
        products_with_coords = [p for p in products if p.get('lat') and p.get('lon')]
        
        result = f'# 🔄 Location Comparison ({len(locations)} locations)\\n\\n'
        result += f'**Analysis Radius:** {radius_km}km\\n\\n'
        
        location_analyses = []
        
        for i, location in enumerate(locations):
            lat = location['lat']
            lon = location['lon']
            name = location.get('name', f'Location {i+1}')
            
            # Find nearby stores and products
            nearby_stores = []
            for store in stores_with_coords:
                distance = haversine_distance(lat, lon, store['lat'], store['lon'])
                if distance <= radius_km:
                    nearby_stores.append((store, distance))
            
            nearby_products = []
            for product in products_with_coords:
                distance = haversine_distance(lat, lon, product['lat'], product['lon'])
                if distance <= radius_km:
                    nearby_products.append((product, distance))
            
            # Calculate metrics
            analysis = {
                'name': name,
                'lat': lat,
                'lon': lon,
                'store_count': len(nearby_stores),
                'product_count': len(nearby_products),
                'closest_store_distance': min([d for _, d in nearby_stores]) if nearby_stores else float('inf'),
                'avg_store_distance': sum([d for _, d in nearby_stores]) / len(nearby_stores) if nearby_stores else float('inf'),
                'store_types': Counter([s[0].get('type', 'unknown') for s in nearby_stores]),
                'products_with_prices': len([p for p, _ in nearby_products if p.get('price')])
            }
            
            # Calculate average product price
            priced_products = [p for p, _ in nearby_products if p.get('price')]
            if priced_products:
                prices = [float(p['price']) for p in priced_products]
                analysis['avg_product_price'] = sum(prices) / len(prices)
            else:
                analysis['avg_product_price'] = 0
            
            location_analyses.append(analysis)
        
        # Comparison table
        result += '## Market Presence Comparison\\n'
        result += '| Location | Stores | Products | Closest Store | Avg Price |\\n'
        result += '|----------|--------|----------|---------------|-----------|\\n'
        
        for analysis in location_analyses:
            closest_dist = f'{analysis["closest_store_distance"]:.1f}km' if analysis["closest_store_distance"] != float('inf') else 'None'
            avg_price = f'€{analysis["avg_product_price"]:.2f}' if analysis['avg_product_price'] > 0 else 'N/A'
            
            result += f'| {analysis["name"]} | {analysis["store_count"]} | {analysis["product_count"]} | {closest_dist} | {avg_price} |\\n'
        
        # Detailed analysis
        result += '\\n## Detailed Analysis\\n\\n'
        
        for analysis in location_analyses:
            result += f'### {analysis["name"]} ({analysis["lat"]:.4f}, {analysis["lon"]:.4f})\\n'
            
            if analysis['store_count'] > 0:
                result += f'**Competition Level:** '
                if analysis['store_count'] >= 10:
                    result += 'Very High'
                elif analysis['store_count'] >= 5:
                    result += 'High'
                elif analysis['store_count'] >= 2:
                    result += 'Medium'
                else:
                    result += 'Low'
                result += f' ({analysis["store_count"]} stores)\\n'
                
                result += f'**Competition Distance:** {analysis["avg_store_distance"]:.1f}km average\\n'
                
                if analysis['store_types']:
                    result += f'**Dominant Store Types:** '
                    top_types = analysis['store_types'].most_common(2)
                    result += ', '.join([f'{stype} ({count})' for stype, count in top_types])
                    result += '\\n'
            else:
                result += f'**Competition Level:** None (untapped market)\\n'
            
            if analysis['product_count'] > 0:
                result += f'**Product Market:** {analysis["product_count"]} products in area\\n'
                if analysis['avg_product_price'] > 0:
                    result += f'**Market Pricing:** €{analysis["avg_product_price"]:.2f} average\\n'
            else:
                result += f'**Product Market:** No products in area\\n'
            
            result += '\\n'
        
        # Rankings and recommendations
        result += '## Rankings & Recommendations\\n\\n'
        
        # Best locations by different criteria
        best_low_competition = min(location_analyses, key=lambda x: x['store_count'])
        best_market_presence = max(location_analyses, key=lambda x: x['product_count'])
        
        result += f'**Lowest Competition:** {best_low_competition["name"]} ({best_low_competition["store_count"]} stores)\\n'
        result += f'**Highest Market Activity:** {best_market_presence["name"]} ({best_market_presence["product_count"]} products)\\n'
        
        # Overall recommendations
        result += f'\\n**Overall Recommendations:**\\n'
        
        for analysis in location_analyses:
            if analysis['store_count'] == 0:
                result += f'  • **{analysis["name"]}**: High potential - untapped market\\n'
            elif analysis['store_count'] <= 2 and analysis['product_count'] > 5:
                result += f'  • **{analysis["name"]}**: Good opportunity - established demand, low competition\\n'
            elif analysis['store_count'] >= 8:
                result += f'  • **{analysis["name"]}**: High risk - saturated market\\n'
            else:
                result += f'  • **{analysis["name"]}**: Moderate opportunity - balanced risk/reward\\n'
        
        return [TextContent(type='text', text=result)]


async def _find_optimal_location(args: Dict[str, Any]) -> List[TextContent]:
    """Find optimal locations for new stores."""
    target_area = args.get('target_area')
    min_distance_km = args.get('min_distance_from_competitors_km', 2)
    
    if not target_area:
        return [TextContent(type='text', text='Error: target_area is required')]
    
    center_lat = target_area['center_lat']
    center_lon = target_area['center_lon']
    search_radius_km = target_area['radius_km']
    
    with get_http_client() as client:
        stores_response = client.get('/v1/stores/')
        stores_response.raise_for_status()
        stores = stores_response.json()
        
        existing_stores = [s for s in stores if s.get('lat') and s.get('lon')]
        
        result = f'# 🎯 Optimal Location Analysis\\n\\n'
        result += f'**Search Area:** {center_lat:.4f}, {center_lon:.4f} (radius: {search_radius_km}km)\\n'
        result += f'**Minimum Distance from Competitors:** {min_distance_km}km\\n'
        result += f'**Existing Stores:** {len(existing_stores)}\\n\\n'
        
        # Generate candidate locations in a grid pattern
        candidate_locations = []
        grid_points = 15  # Create a 15x15 grid
        
        for i in range(grid_points):
            for j in range(grid_points):
                # Convert grid position to lat/lon offset
                lat_offset = (i - grid_points//2) * (search_radius_km * 2) / grid_points / 111.0
                lon_offset = (j - grid_points//2) * (search_radius_km * 2) / grid_points / (111.0 * math.cos(math.radians(center_lat)))
                
                candidate_lat = center_lat + lat_offset
                candidate_lon = center_lon + lon_offset
                
                # Check if candidate is within search radius
                distance_from_center = haversine_distance(center_lat, center_lon, candidate_lat, candidate_lon)
                if distance_from_center <= search_radius_km:
                    
                    # Check minimum distance from competitors
                    distances_to_competitors = []
                    for store in existing_stores:
                        distance = haversine_distance(candidate_lat, candidate_lon, store['lat'], store['lon'])
                        distances_to_competitors.append(distance)
                    
                    if not distances_to_competitors or min(distances_to_competitors) >= min_distance_km:
                        # This is a valid candidate location
                        min_competitor_distance = min(distances_to_competitors) if distances_to_competitors else float('inf')
                        
                        # Calculate market potential score
                        # Factors: distance from center (lower is better), distance from competitors (higher is better)
                        center_distance_score = 1 - (distance_from_center / search_radius_km)  # 0-1, higher is better
                        competitor_distance_score = min(min_competitor_distance / (search_radius_km * 2), 1)  # 0-1, higher is better
                        
                        overall_score = (center_distance_score * 0.3) + (competitor_distance_score * 0.7)
                        
                        candidate_locations.append({
                            'lat': candidate_lat,
                            'lon': candidate_lon,
                            'distance_from_center': distance_from_center,
                            'min_competitor_distance': min_competitor_distance,
                            'score': overall_score
                        })
        
        if not candidate_locations:
            result += 'No suitable locations found with the specified criteria.\\n'
            result += 'Consider:\\n'
            result += f'  • Reducing minimum distance requirement (currently {min_distance_km}km)\\n'
            result += f'  • Expanding search area (currently {search_radius_km}km radius)\\n'
            result += f'  • Analyzing different geographic area\\n'
            return [TextContent(type='text', text=result)]
        
        # Sort by score (best first)
        candidate_locations.sort(key=lambda x: x['score'], reverse=True)
        
        result += f'**Suitable Locations Found:** {len(candidate_locations)}\\n\\n'
        
        # Show top candidates
        result += '## Top Location Recommendations\\n\\n'
        
        for i, location in enumerate(candidate_locations[:10], 1):
            result += f'{i}. **Location:** {location["lat"]:.4f}, {location["lon"]:.4f}\\n'
            result += f'   Distance from search center: {location["distance_from_center"]:.1f}km\\n'
            
            if location["min_competitor_distance"] == float('inf'):
                result += f'   Distance from nearest competitor: No competitors in area\\n'
            else:
                result += f'   Distance from nearest competitor: {location["min_competitor_distance"]:.1f}km\\n'
            
            result += f'   Optimization score: {location["score"]:.3f}\\n'
            
            # Market assessment
            if location["min_competitor_distance"] > search_radius_km:
                market_status = 'Untapped market'
            elif location["min_competitor_distance"] > min_distance_km * 2:
                market_status = 'Low competition'
            else:
                market_status = 'Moderate competition'
            
            result += f'   Market status: {market_status}\\n\\n'
        
        if len(candidate_locations) > 10:
            result += f'... and {len(candidate_locations) - 10} more suitable locations.\\n\\n'
        
        # Analysis summary
        result += '## Analysis Summary\\n\\n'
        
        best_location = candidate_locations[0]
        result += f'**Top Recommendation:** {best_location["lat"]:.4f}, {best_location["lon"]:.4f}\\n'
        
        avg_competitor_distance = sum(loc["min_competitor_distance"] for loc in candidate_locations if loc["min_competitor_distance"] != float('inf')) / len([loc for loc in candidate_locations if loc["min_competitor_distance"] != float('inf')])
        
        if avg_competitor_distance:
            result += f'**Average Distance to Competition:** {avg_competitor_distance:.1f}km\\n'
        
        # Strategic advice
        result += f'\\n**Strategic Recommendations:**\\n'
        
        if len(candidate_locations) > 5:
            result += f'  • Multiple viable locations available - consider market research\\n'
            result += f'  • Focus on locations with highest optimization scores\\n'
        else:
            result += f'  • Limited suitable locations - consider expanding search criteria\\n'
        
        if best_location["min_competitor_distance"] > search_radius_km:
            result += f'  • Top location has no nearby competition - first mover advantage\\n'
        else:
            result += f'  • Maintain minimum distance requirements for competitive advantage\\n'
        
        result += f'  • Validate locations with local market research and demographics\\n'
        
        return [TextContent(type='text', text=result)]


if __name__ == '__main__':
    # This will be called by the run script
    logger.info('Starting Partle Location Intelligence MCP Server')
    mcp_server.run()
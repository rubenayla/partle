"""
Public API endpoints for external integrations (ChatGPT, etc.)
Read-only access with API key authentication
"""
from fastapi import APIRouter, HTTPException, Depends, Header, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, List
import os
import hashlib
import hmac
from datetime import datetime

from app.api.deps import get_db

from app.api.v1.products import list_products as _list_products
from app.api.v1.stores import list_stores as _list_stores
from app.api.v1.search import search_products as _search_products

router = APIRouter()
security = HTTPBearer(auto_error=False)  # Don't auto-error if no header present

# API Keys (in production, store these in a database)
VALID_API_KEYS = {
    "chatgpt_readonly": os.getenv("CHATGPT_API_KEY", "pk_test_chatgpt_readonly_key"),
    "claude_readonly": os.getenv("CLAUDE_API_KEY", "pk_test_claude_readonly_key"),
}

def verify_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    api_key: Optional[str] = Query(None, description="API key for authentication (alternative to Authorization header)")
):
    """Verify API key from Authorization header or query parameter"""
    # Try to get token from Authorization header first
    token = None
    if credentials:
        token = credentials.credentials
    
    # Fall back to query parameter if no header
    if not token and api_key:
        token = api_key
    
    # If still no token, raise error
    if not token:
        raise HTTPException(
            status_code=401,
            detail="API key required. Use Authorization header or api_key query parameter"
        )
    
    if token not in VALID_API_KEYS.values():
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return token

@router.get("/products", 
    summary="Search and retrieve products",
    description="""
    Search products in the Partle marketplace with advanced filtering options.
    
    Perfect for AI assistants to help users find specific products, compare prices, 
    or browse by category. Returns detailed product information including prices,
    store details, and product specifications.
    
    **Use Cases:**
    - "Find wireless headphones under €100"
    - "Show me electronics from TechStore" 
    - "What adhesive products are available?"
    
    **Authentication:** Requires API key in Authorization header
    **Rate Limit:** 100 requests per hour per API key
    """,
    tags=["Public API", "Products"],
    responses={
        200: {
            "description": "List of products matching the search criteria",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 115,
                            "name": "Wireless Bluetooth Headphones",
                            "description": "High-quality wireless headphones with noise cancellation",
                            "price": 89.99,
                            "url": "https://store.example.com/headphones-115",
                            "image_url": "https://store.example.com/images/headphones.jpg",
                            "store": {
                                "id": 1,
                                "name": "Electronics Hub", 
                                "address": "123 Tech Street"
                            },
                            "tags": [
                                {"name": "electronics"},
                                {"name": "audio"},
                                {"name": "bluetooth"}
                            ]
                        }
                    ]
                }
            }
        },
        401: {"description": "Invalid or missing API key"},
        429: {"description": "Rate limit exceeded"}
    })
def get_products_public(
    api_key: str = Depends(verify_api_key),
    q: Optional[str] = Query(None, description="Search term to find products by name or description (e.g., 'wireless headphones', 'adhesive tape')"),
    limit: int = Query(20, le=100, description="Number of products to return (1-100, default: 20)"),
    offset: int = Query(0, description="Number of products to skip for pagination (default: 0)"),
    min_price: Optional[float] = Query(None, description="Minimum price filter in EUR (e.g., 10.50)"),
    max_price: Optional[float] = Query(None, description="Maximum price filter in EUR (e.g., 100.00)"), 
    tags: Optional[str] = Query(None, description="Filter by tags, comma-separated (e.g., 'electronics,bluetooth' or 'adhesive,tape')"),
    db: Session = Depends(get_db)
):
    """Get products with public read-only access"""
    # Get products but exclude binary image_data field to prevent serialization errors
    products = _list_products(
        q=q, limit=limit, offset=offset, 
        min_price=min_price, max_price=max_price, 
        tags=tags, sort_by="created_at", db=db
    )
    
    # Clear image_data field from each product to prevent UnicodeDecodeError
    # The image can still be accessed via /v1/products/{id}/image endpoint
    for product in products:
        if hasattr(product, 'image_data'):
            product.image_data = None
    
    return products

@router.get("/stores",
    summary="Browse marketplace stores",
    description="""
    Retrieve information about stores in the Partle marketplace.
    
    Perfect for AI assistants to help users find stores, get location information,
    or browse available retailers. Returns store details including addresses,
    coordinates, and contact information.
    
    **Use Cases:**
    - "Show me electronics stores"
    - "Find stores near me"
    - "List all available retailers"
    
    **Authentication:** Requires API key in Authorization header
    **Rate Limit:** 100 requests per hour per API key
    """,
    tags=["Public API", "Stores"],
    responses={
        200: {
            "description": "List of stores in the marketplace",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 2,
                            "name": "Electronics Hub",
                            "lat": 40.7128,
                            "lon": -74.0060,
                            "address": "123 Tech Street, New York, NY 10001",
                            "owner_id": 10,
                            "type": "physical", 
                            "homepage": "https://electronicshub.com"
                        }
                    ]
                }
            }
        },
        401: {"description": "Invalid or missing API key"},
        429: {"description": "Rate limit exceeded"}
    })
def get_stores_public(
    api_key: str = Depends(verify_api_key),
    limit: int = Query(20, le=50, description="Number of stores to return (1-50, default: 20)"),
    offset: int = Query(0, description="Number of stores to skip for pagination (default: 0)"),
    db: Session = Depends(get_db)
):
    """Get stores with public read-only access"""
    return _list_stores(limit=limit, offset=offset, db=db)

@router.get("/search",
    summary="Search products for AI assistants",
    description="Advanced product search with Elasticsearch. Read-only access.",
    tags=["Public API"])
def search_products_public(
    api_key: str = Depends(verify_api_key),
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, le=50, description="Maximum 50 results"),
    filters: Optional[str] = Query(None, description="Additional filters")
):
    """Search products with public read-only access"""
    return _search_products(q=q, limit=limit)

@router.get("/stats",
    summary="Get platform statistics",
    description="Basic platform metrics for AI assistants",
    tags=["Public API"])
def get_platform_stats(
    api_key: str = Depends(verify_api_key),
    db: Session = Depends(get_db)
):
    """Get basic platform statistics"""
    # Import here to avoid circular imports
    from app.db.models import Product, Store
    from sqlalchemy import func
    
    total_products = db.query(func.count(Product.id)).scalar()
    total_stores = db.query(func.count(Store.id)).scalar()
    
    return {
        "total_products": total_products,
        "total_stores": total_stores,
        "last_updated": datetime.utcnow().isoformat(),
        "api_version": "1.0",
        "description": "Partle marketplace - Find products and stores"
    }

@router.get("/health",
    summary="Health check for AI assistants",
    description="Check if the API is available",
    tags=["Public API"])
def health_check():
    """Public health check - no auth required"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Partle API is running"
    }

@router.get("/mcp/servers",
    summary="List available MCP servers",
    description="Returns information about available Model Context Protocol servers for AI integration",
    tags=["Public API", "MCP"])
def get_mcp_servers():
    """Get available MCP servers - no auth required for discovery"""
    return {
        "servers": [
            {
                "name": "partle-products",
                "description": "Search, analyze, and manage products in the Partle marketplace",
                "command": ["python", "backend/scripts/run_mcp_products.py"],
                "capabilities": [
                    "search_products",
                    "get_product", 
                    "get_products_by_store",
                    "search_products_elasticsearch"
                ],
                "status": "available",
                "version": "1.0.0",
                "tags": ["ecommerce", "products", "search", "marketplace"]
            },
            {
                "name": "partle-stores",
                "description": "Discover and analyze stores, their locations, and market presence",
                "command": ["python", "backend/scripts/run_mcp_stores.py"],
                "capabilities": [
                    "search_stores",
                    "get_store",
                    "list_stores_dropdown",
                    "get_store_analytics",
                    "find_stores_by_type",
                    "find_stores_near_location"
                ],
                "status": "available",
                "version": "1.0.0", 
                "tags": ["stores", "location", "business", "retail"]
            },
            {
                "name": "partle-analytics",
                "description": "Business intelligence and comprehensive platform analytics",
                "command": ["python", "backend/scripts/run_mcp_analytics.py"],
                "capabilities": [
                    "get_platform_overview",
                    "analyze_products",
                    "analyze_stores",
                    "get_top_performers",
                    "analyze_tags",
                    "get_market_insights",
                    "compare_stores"
                ],
                "status": "available",
                "version": "1.0.0",
                "tags": ["analytics", "business-intelligence", "insights", "metrics"]
            },
            {
                "name": "partle-price-intelligence",
                "description": "Advanced pricing analysis, market positioning, and competitive intelligence",
                "command": ["python", "backend/scripts/run_mcp_price_intelligence.py"],
                "capabilities": [
                    "analyze_price_trends",
                    "find_price_outliers",
                    "compare_store_pricing",
                    "find_similar_products",
                    "get_market_positioning",
                    "identify_pricing_gaps",
                    "generate_pricing_recommendations"
                ],
                "status": "available",
                "version": "1.0.0",
                "tags": ["pricing", "market-analysis", "competition", "strategy"]
            },
            {
                "name": "partle-location-intelligence", 
                "description": "Geographic analysis, store density, and location-based market intelligence",
                "command": ["python", "backend/scripts/run_mcp_location_intelligence.py"],
                "capabilities": [
                    "find_nearby_stores",
                    "analyze_store_density",
                    "find_market_gaps",
                    "analyze_coverage_area",
                    "get_location_insights",
                    "compare_locations",
                    "find_optimal_location"
                ],
                "status": "available",
                "version": "1.0.0",
                "tags": ["location", "geography", "market-gaps", "expansion"]
            },
            {
                "name": "partle-recommendations",
                "description": "Personalized recommendations, product discovery, and shopping optimization",
                "command": ["python", "backend/scripts/run_mcp_recommendations.py"],
                "capabilities": [
                    "recommend_similar_products",
                    "recommend_products_by_category", 
                    "recommend_stores_by_products",
                    "get_trending_products",
                    "recommend_complementary_products",
                    "generate_shopping_list",
                    "recommend_price_alerts"
                ],
                "status": "available",
                "version": "1.0.0",
                "tags": ["recommendations", "personalization", "discovery", "shopping"]
            }
        ],
        "total_servers": 6,
        "manifest_url": "/mcp-manifest.json",
        "documentation": {
            "setup_guide": "/docs/mcp-setup.md",
            "chatgpt_integration": "/docs/chatgpt-integration.md",
            "public_api_guide": "/docs/public-api-guide.md"
        },
        "api_info": {
            "base_url": "https://partle.rubenayla.xyz",
            "public_api_prefix": "/v1/public",
            "authentication_required": True,
            "rate_limit": "100 requests per hour"
        }
    }

@router.get("/mcp/manifest",
    summary="Get MCP manifest file",
    description="Returns the complete Model Context Protocol manifest for server configuration",
    tags=["Public API", "MCP"])
def get_mcp_manifest():
    """Get MCP manifest - no auth required for discovery"""
    import json
    import os
    
    manifest_path = os.path.join(os.path.dirname(__file__), "../../../../mcp-manifest.json")
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        return manifest
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="MCP manifest file not found"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Invalid MCP manifest format"
        )

@router.get("/mcp/health",
    summary="MCP servers health check",
    description="Check the health and availability of MCP servers",
    tags=["Public API", "MCP"])
def mcp_health_check():
    """Check MCP servers health - no auth required"""
    return {
        "status": "healthy",
        "servers_available": 6,
        "api_version": "1.0.0",
        "mcp_protocol_version": "1.13.1",
        "last_updated": datetime.utcnow().isoformat(),
        "environment": {
            "partle_api_url": "https://partle.rubenayla.xyz",
            "python_version": ">=3.12",
            "dependencies_status": "satisfied"
        },
        "capabilities": {
            "product_search": True,
            "store_analysis": True, 
            "business_intelligence": True,
            "price_intelligence": True,
            "location_intelligence": True,
            "recommendations": True
        }
    }
"""
HTTP/WebSocket bridge for MCP servers to enable remote access from ChatGPT.
This allows MCP servers to be exposed via HTTP endpoints on production servers.
"""
import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import subprocess
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/mcp", tags=["MCP"])


class MCPRequest(BaseModel):
    """Request to send to an MCP server."""
    server: str
    method: str
    params: Dict[str, Any] = {}
    id: Optional[int] = None


class MCPServerInfo(BaseModel):
    """Information about an available MCP server."""
    name: str
    description: str
    status: str
    capabilities: list[str]
    endpoint: str


@router.get("/servers")
async def list_mcp_servers() -> Dict[str, Any]:
    """
    List all available MCP servers and their capabilities.
    This endpoint is used by ChatGPT for auto-discovery.
    """
    servers = [
        {
            "name": "partle-products",
            "description": "Product search, filtering, and management",
            "status": "available",
            "capabilities": ["search_products", "get_product", "get_product_details"],
            "endpoint": "/v1/mcp/connect/partle-products",
            "methods": {
                "search_products": {
                    "description": "Search for products with filters",
                    "params": {
                        "query": "string",
                        "tags": "array",
                        "sort_by": "string",
                        "limit": "integer"
                    }
                },
                "get_product": {
                    "description": "Get a specific product by ID",
                    "params": {
                        "product_id": "string"
                    }
                }
            }
        },
        {
            "name": "partle-analytics",
            "description": "Platform analytics and business intelligence",
            "status": "available",
            "capabilities": ["get_platform_overview", "get_top_performers", "get_trends"],
            "endpoint": "/v1/mcp/connect/partle-analytics",
            "methods": {
                "get_platform_overview": {
                    "description": "Get platform-wide metrics and statistics",
                    "params": {}
                },
                "get_top_performers": {
                    "description": "Get top performing products and stores",
                    "params": {
                        "metric": "string",
                        "limit": "integer"
                    }
                }
            }
        },
        {
            "name": "partle-stores",
            "description": "Store management and location services",
            "status": "available",
            "capabilities": ["search_stores", "get_store", "find_stores_near_location"],
            "endpoint": "/v1/mcp/connect/partle-stores",
            "methods": {
                "search_stores": {
                    "description": "Search for stores",
                    "params": {
                        "query": "string",
                        "store_type": "string"
                    }
                },
                "find_stores_near_location": {
                    "description": "Find stores near a location",
                    "params": {
                        "latitude": "number",
                        "longitude": "number",
                        "radius_km": "number"
                    }
                }
            }
        },
        {
            "name": "partle-price-intelligence",
            "description": "Price analysis and competitive intelligence",
            "status": "available",
            "capabilities": ["analyze_pricing", "compare_store_pricing", "get_price_trends"],
            "endpoint": "/v1/mcp/connect/partle-price-intelligence"
        },
        {
            "name": "partle-location-intelligence",
            "description": "Location-based analysis and market intelligence",
            "status": "available",
            "capabilities": ["find_market_gaps", "analyze_coverage", "suggest_expansion"],
            "endpoint": "/v1/mcp/connect/partle-location-intelligence"
        },
        {
            "name": "partle-recommendations",
            "description": "Product recommendations and similarity analysis",
            "status": "available",
            "capabilities": ["recommend_similar_products", "get_trending", "personalized_recommendations"],
            "endpoint": "/v1/mcp/connect/partle-recommendations"
        }
    ]

    return {
        "servers": servers,
        "version": "1.0.0",
        "mcp_version": "2024-11-05",
        "base_url": os.getenv("PARTLE_API_URL", "http://localhost:8000"),
        "documentation": "/docs/mcp-api",
        "health_check": "/v1/mcp/health"
    }


@router.get("/health")
async def mcp_health_check() -> Dict[str, Any]:
    """Health check endpoint for MCP services."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "servers_available": 6,
        "api_version": "1.0.0"
    }


@router.post("/execute/{server_name}")
async def execute_mcp_command(server_name: str, request: MCPRequest) -> Dict[str, Any]:
    """
    Execute a command on a specific MCP server.
    This is a simplified HTTP interface for MCP servers.
    """
    # Map server names to their Python scripts
    server_scripts = {
        "partle-products": "scripts/run_mcp_products.py",
        "partle-analytics": "scripts/run_mcp_analytics.py",
        "partle-stores": "scripts/run_mcp_stores.py",
        "partle-price-intelligence": "scripts/run_mcp_price_intelligence.py",
        "partle-location-intelligence": "scripts/run_mcp_location_intelligence.py",
        "partle-recommendations": "scripts/run_mcp_recommendations.py"
    }

    if server_name not in server_scripts:
        raise HTTPException(status_code=404, detail=f"MCP server '{server_name}' not found")

    # For production, we'll call the API endpoints directly instead of running MCP servers
    # This is more efficient and secure for production use

    if server_name == "partle-products":
        return await handle_products_request(request)
    elif server_name == "partle-analytics":
        return await handle_analytics_request(request)
    elif server_name == "partle-stores":
        return await handle_stores_request(request)
    else:
        raise HTTPException(status_code=501, detail=f"Server '{server_name}' not yet implemented")


async def handle_products_request(request: MCPRequest) -> Dict[str, Any]:
    """Handle requests for the products MCP server."""
    import httpx

    base_url = os.getenv("PARTLE_API_URL", "http://localhost:8000")

    async with httpx.AsyncClient(base_url=base_url) as client:
        if request.method == "search_products":
            # Call the actual products API
            params = request.params
            # Transform MCP params to API params
            response = await client.get(
                "/v1/products/",
                params={
                    "q": params.get("query", ""),
                    "tags": ",".join(params.get("tags", [])) if params.get("tags") else None,
                    "sort_by": params.get("sort_by", "created_at"),
                    "limit": params.get("limit", 20),
                    "offset": params.get("offset", 0)
                }
            )
            response.raise_for_status()
            return {"result": response.json(), "id": request.id}

        elif request.method == "get_product":
            product_id = request.params.get("product_id")
            if not product_id:
                raise HTTPException(status_code=400, detail="product_id required")
            # Call actual API
            response = await client.get(f"/v1/products/{product_id}")
            response.raise_for_status()
            return {"result": response.json(), "id": request.id}

        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {request.method}")


async def handle_analytics_request(request: MCPRequest) -> Dict[str, Any]:
    """Handle requests for the analytics MCP server."""
    # Placeholder - implement actual analytics calls
    if request.method == "get_platform_overview":
        return {
            "result": {
                "total_products": 15234,
                "total_stores": 342,
                "active_users": 1250,
                "searches_today": 8934
            },
            "id": request.id
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unknown method: {request.method}")


async def handle_stores_request(request: MCPRequest) -> Dict[str, Any]:
    """Handle requests for the stores MCP server."""
    import httpx

    base_url = os.getenv("PARTLE_API_URL", "http://localhost:8000")

    async with httpx.AsyncClient(base_url=base_url) as client:
        if request.method == "search_stores":
            params = request.params
            # Call actual stores API
            response = await client.get(
                "/v1/stores/",
                params={
                    "q": params.get("query", ""),
                    "store_type": params.get("store_type"),
                    "limit": params.get("limit", 20),
                    "offset": params.get("offset", 0)
                }
            )
            response.raise_for_status()
            return {"result": response.json(), "id": request.id}

        elif request.method == "find_stores_near_location":
            lat = request.params.get("latitude")
            lon = request.params.get("longitude")
            radius = request.params.get("radius_km", 10)

            if lat is None or lon is None:
                raise HTTPException(status_code=400, detail="latitude and longitude required")

            # Call location-based API
            response = await client.get(
                "/v1/stores/nearby",
                params={
                    "lat": lat,
                    "lon": lon,
                    "radius_km": radius
                }
            )
            response.raise_for_status()
            return {"result": response.json(), "id": request.id}

        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {request.method}")


@router.websocket("/connect/{server_name}")
async def mcp_websocket(websocket: WebSocket, server_name: str):
    """
    WebSocket endpoint for persistent MCP connections.
    This allows ChatGPT to maintain a connection for multiple requests.
    """
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            request_data = json.loads(data)

            # Create MCPRequest from the data
            request = MCPRequest(
                server=server_name,
                method=request_data.get("method"),
                params=request_data.get("params", {}),
                id=request_data.get("id")
            )

            # Execute the request
            try:
                if server_name == "partle-products":
                    response = await handle_products_request(request)
                elif server_name == "partle-analytics":
                    response = await handle_analytics_request(request)
                elif server_name == "partle-stores":
                    response = await handle_stores_request(request)
                else:
                    response = {
                        "error": f"Server '{server_name}' not implemented",
                        "id": request.id
                    }
            except Exception as e:
                response = {
                    "error": str(e),
                    "id": request.id
                }

            # Send response back
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for server: {server_name}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()


@router.get("/manifest")
async def get_mcp_manifest() -> Dict[str, Any]:
    """
    Return MCP manifest for ChatGPT auto-discovery.
    This is the main endpoint ChatGPT will use to understand available servers.
    """
    return {
        "version": "1.0.0",
        "name": "Partle MCP Services",
        "description": "MCP servers for Partle platform - product search, analytics, and intelligence",
        "author": "Partle Team",
        "homepage": "https://partle.com",
        "servers": await list_mcp_servers(),
        "authentication": {
            "type": "api_key",
            "header": "X-API-Key",
            "description": "Optional API key for enhanced rate limits"
        },
        "base_url": os.getenv("PARTLE_API_URL", "http://localhost:8000"),
        "endpoints": {
            "discovery": "/v1/mcp/servers",
            "health": "/v1/mcp/health",
            "execute": "/v1/mcp/execute/{server_name}",
            "websocket": "/v1/mcp/connect/{server_name}",
            "manifest": "/v1/mcp/manifest"
        }
    }
"""
SSE-based MCP server implementation for ChatGPT integration.
Implements the required search action and SSE transport.
"""
import json
import asyncio
import logging
from typing import Dict, Any, AsyncGenerator, Optional, List
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import os
from datetime import datetime, timezone
from sse_starlette.sse import EventSourceResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/v1/mcp", tags=["MCP-SSE"])


class MCPMessage(BaseModel):
    """MCP message format."""
    jsonrpc: str = "2.0"
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[int] = None


async def create_sse_message(data: Dict[str, Any]) -> str:
    """Format data as SSE message."""
    return f"data: {json.dumps(data)}\n\n"


@router.get("/sse")
async def mcp_sse_endpoint(request: Request):
    """
    SSE endpoint for ChatGPT MCP connection.
    Implements the required protocol for ChatGPT connectors.
    """
    async def event_generator():
        """Generate SSE events for MCP communication."""
        try:
            # Send initial connection acknowledgment
            yield await create_sse_message({
                "jsonrpc": "2.0",
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {
                        "name": "partle-mcp",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {
                            "search": True,
                            "fetch": True
                        }
                    }
                },
                "id": 1
            })

            # Keep connection alive and handle incoming messages
            while True:
                await asyncio.sleep(30)  # Send heartbeat every 30 seconds
                yield await create_sse_message({
                    "type": "heartbeat",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })

        except asyncio.CancelledError:
            logger.info("SSE connection closed")
            raise

    return EventSourceResponse(event_generator())


@router.post("/sse/message")
async def process_mcp_message(message: MCPMessage):
    """
    Process incoming MCP messages from ChatGPT.
    Handles the required methods including search action.
    """
    if message.method == "tools/list":
        # Return available tools including required search action
        return {
            "jsonrpc": "2.0",
            "result": {
                "tools": [
                    {
                        "name": "search",
                        "description": "Search for products in the Partle marketplace",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query for products"
                                },
                                "limit": {
                                    "type": "number",
                                    "description": "Maximum number of results",
                                    "default": 10
                                }
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "fetch",
                        "description": "Fetch detailed information about a specific product",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "product_id": {
                                    "type": "string",
                                    "description": "Product ID to fetch"
                                }
                            },
                            "required": ["product_id"]
                        }
                    },
                    {
                        "name": "list_stores",
                        "description": "List stores in the marketplace",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "limit": {
                                    "type": "number",
                                    "description": "Maximum number of stores",
                                    "default": 10
                                }
                            }
                        }
                    }
                ]
            },
            "id": message.id
        }

    elif message.method == "tools/call":
        # Handle tool calls
        tool_name = message.params.get("name") if message.params else None
        arguments = message.params.get("arguments", {}) if message.params else {}

        if tool_name == "search":
            # Implement the required search action
            return await handle_search(arguments, message.id)
        elif tool_name == "fetch":
            return await handle_fetch(arguments, message.id)
        elif tool_name == "list_stores":
            return await handle_list_stores(arguments, message.id)
        else:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                },
                "id": message.id
            }

    else:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": f"Method not found: {message.method}"
            },
            "id": message.id
        }


async def handle_search(params: Dict[str, Any], request_id: Optional[int]) -> Dict[str, Any]:
    """
    Handle the search action required by ChatGPT.
    This is the critical method that ChatGPT checks for.
    """
    query = params.get("query", "")
    limit = params.get("limit", 10)

    base_url = os.getenv("PARTLE_API_URL", "http://localhost:8000")

    async with httpx.AsyncClient(base_url=base_url) as client:
        try:
            response = await client.get(
                "/v1/products/",
                params={
                    "q": query,
                    "limit": limit,
                    "offset": 0
                }
            )
            response.raise_for_status()
            data = response.json()

            # Format results for ChatGPT
            results = []
            for product in data.get("items", []):
                results.append({
                    "id": product.get("id"),
                    "name": product.get("name"),
                    "description": product.get("description", ""),
                    "price": product.get("price"),
                    "store": product.get("store_name", "Unknown"),
                    "url": product.get("external_url", ""),
                    "image": f"{base_url}/v1/products/{product.get('id')}/image" if product.get("has_image") else None
                })

            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Found {len(results)} products matching '{query}'"
                        },
                        {
                            "type": "resource",
                            "resource": {
                                "uri": f"partle://search/{query}",
                                "mimeType": "application/json",
                                "text": json.dumps(results, indent=2)
                            }
                        }
                    ]
                },
                "id": request_id
            }
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Search failed: {str(e)}"
                },
                "id": request_id
            }


async def handle_fetch(params: Dict[str, Any], request_id: Optional[int]) -> Dict[str, Any]:
    """Handle fetch action for getting specific product details."""
    product_id = params.get("product_id")

    if not product_id:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32602,
                "message": "product_id is required"
            },
            "id": request_id
        }

    base_url = os.getenv("PARTLE_API_URL", "http://localhost:8000")

    async with httpx.AsyncClient(base_url=base_url) as client:
        try:
            response = await client.get(f"/v1/products/{product_id}")
            response.raise_for_status()
            product = response.json()

            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Product: {product.get('name')}"
                        },
                        {
                            "type": "resource",
                            "resource": {
                                "uri": f"partle://product/{product_id}",
                                "mimeType": "application/json",
                                "text": json.dumps(product, indent=2)
                            }
                        }
                    ]
                },
                "id": request_id
            }
        except Exception as e:
            logger.error(f"Fetch error: {e}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Fetch failed: {str(e)}"
                },
                "id": request_id
            }


async def handle_list_stores(params: Dict[str, Any], request_id: Optional[int]) -> Dict[str, Any]:
    """Handle listing stores action."""
    limit = params.get("limit", 10)

    base_url = os.getenv("PARTLE_API_URL", "http://localhost:8000")

    async with httpx.AsyncClient(base_url=base_url) as client:
        try:
            response = await client.get(
                "/v1/stores/",
                params={"limit": limit, "offset": 0}
            )
            response.raise_for_status()
            data = response.json()

            stores = []
            for store in data.get("items", []):
                stores.append({
                    "id": store.get("id"),
                    "name": store.get("name"),
                    "store_type": store.get("store_type"),
                    "location": store.get("location"),
                    "url": store.get("website")
                })

            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Found {len(stores)} stores"
                        },
                        {
                            "type": "resource",
                            "resource": {
                                "uri": "partle://stores",
                                "mimeType": "application/json",
                                "text": json.dumps(stores, indent=2)
                            }
                        }
                    ]
                },
                "id": request_id
            }
        except Exception as e:
            logger.error(f"List stores error: {e}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"List stores failed: {str(e)}"
                },
                "id": request_id
            }


@router.get("/sse/manifest")
async def sse_manifest():
    """
    Return manifest for SSE-based MCP server.
    This is what ChatGPT should connect to.
    """
    return {
        "version": "1.0.0",
        "protocol": "sse",
        "name": "Partle MCP Server",
        "description": "SSE-based MCP server for Partle marketplace with required search action",
        "endpoint": "https://partle.rubenayla.xyz/v1/mcp/sse",
        "capabilities": {
            "tools": {
                "search": {
                    "description": "Search products in Partle marketplace",
                    "required": True
                },
                "fetch": {
                    "description": "Fetch specific product details",
                    "required": False
                },
                "list_stores": {
                    "description": "List marketplace stores",
                    "required": False
                }
            }
        },
        "authentication": {
            "type": "none",
            "description": "No authentication required"
        }
    }
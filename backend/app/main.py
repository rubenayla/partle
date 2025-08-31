# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, external, health, parts, products, stores, tags, search, logs, public
from app.logging_config import configure_logging, LoggingMiddleware, get_logger
from app.middleware.rate_limit import RateLimitMiddleware

# Configure logging first
configure_logging()
logger = get_logger("main")

# Load local .env if present (useful for local development)
if os.getenv("PRODUCTION_MODE") is None:
    from dotenv import load_dotenv

    load_dotenv()

app = FastAPI(
    title="Partle API",
    version="1.0.0",
    description="""
# Partle Marketplace API

The Partle API provides comprehensive access to marketplace data including products, stores, and platform analytics.

## Features

- **Product Search**: Find products by name, price, category, and tags
- **Store Discovery**: Browse stores and their locations  
- **Platform Analytics**: Get business intelligence and statistics
- **AI Integration**: Public API endpoints for ChatGPT, Claude, and other AI assistants
- **MCP Support**: Model Context Protocol servers for advanced AI integrations

## Authentication

Public API endpoints require API key authentication:
```
Authorization: Bearer pk_test_chatgpt_readonly_key
```

## Rate Limits

- **Public API**: 100 requests per hour per API key
- **Rate limit headers**: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset

## AI Integration

- **OpenAPI Schema**: Available at `/openapi.json` for AI assistant configuration
- **Public API**: Optimized endpoints at `/v1/public/` for external integrations  
- **MCP Discovery**: Model Context Protocol server information at `/v1/public/mcp/`

## Links

- **Interactive Documentation**: [/docs](/docs)
- **ReDoc Documentation**: [/redoc](/redoc) 
- **Public API Guide**: [/docs/public-api-guide.md](docs/public-api-guide.md)
- **MCP Integration**: [/docs/chatgpt-integration.md](docs/chatgpt-integration.md)
""",
    contact={
        "name": "Partle Support",
        "url": "https://github.com/rubenayla/partle",
        "email": "support@partle.com"
    },
    license_info={
        "name": "Proprietary",
        "url": "https://github.com/rubenayla/partle/blob/main/LICENSE"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://partle.rubenayla.xyz", 
            "description": "Production server"
        }
    ]
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, calls=100, period=3600)  # 100 requests per hour

# CORS (must be added before routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://partle.rubenayla.xyz", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(parts.router, prefix="/v1/parts", tags=["Parts"])
app.include_router(stores.router, prefix="/v1/stores", tags=["Stores"])
app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/v1/products", tags=["Products"])
app.include_router(external.router, prefix="/v1/external", tags=["External"])
app.include_router(tags.router, prefix="/v1/tags", tags=["Tags"])
app.include_router(search.router, prefix="/v1/search", tags=["Search"])
app.include_router(logs.router, prefix="/v1/logs", tags=["Logs"])
app.include_router(public.router, prefix="/v1/public", tags=["Public API"])
app.include_router(health.router, prefix="/v1")


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"status": "ok", "version": "v1", "docs": "/docs"}

@app.get("/mcp-manifest.json")
def get_mcp_manifest_json():
    """Serve MCP manifest file directly for AI discovery"""
    import json
    import os
    
    manifest_path = os.path.join(os.path.dirname(__file__), "../../mcp-manifest.json")
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        return manifest
    except FileNotFoundError:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="MCP manifest file not found"
        )
    except json.JSONDecodeError:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail="Invalid MCP manifest format"
        )

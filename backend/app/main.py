# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from app.api.v1 import auth, external, health, parts, products, stores, tags, search, logs, public, admin, reviews
from app.api import mcp_bridge, mcp_sse
from app.routes import bulk_import
from datetime import datetime
from app.logging_config import configure_logging, LoggingMiddleware, get_logger
from app.middleware.rate_limit import RateLimitMiddleware

# Configure logging first
configure_logging()
logger = get_logger("main")

# Always load .env file if it exists
from pathlib import Path
from dotenv import load_dotenv

# Load from backend/.env file
backend_env = Path(__file__).parent.parent / '.env'
if backend_env.exists():
    load_dotenv(backend_env, override=True)

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
    allow_origins=[
        "https://partle.rubenayla.xyz",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://192.168.1.117:3000",
        "https://chatgpt.com",
        "https://chat.openai.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(parts.router, prefix="/v1/parts", tags=["Parts"])
app.include_router(stores.router, prefix="/v1/stores", tags=["Stores"])
app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/v1/products", tags=["Products"])
app.include_router(reviews.router, prefix="/v1/products", tags=["Reviews"])
app.include_router(external.router, prefix="/v1/external", tags=["External"])
app.include_router(tags.router, prefix="/v1/tags", tags=["Tags"])
app.include_router(search.router, prefix="/v1/search", tags=["Search"])
app.include_router(logs.router, prefix="/v1/logs", tags=["Logs"])
app.include_router(public.router, prefix="/v1/public", tags=["Public API"])
app.include_router(admin.router, prefix="/v1/admin", tags=["Admin"])
app.include_router(bulk_import.router, tags=["Bulk Import"])  # Bulk import endpoints
app.include_router(mcp_bridge.router)  # MCP bridge endpoints at /v1/mcp
app.include_router(mcp_sse.router)  # SSE-based MCP endpoints for ChatGPT
app.include_router(health.router, prefix="/v1")


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"status": "ok", "version": "v1", "docs": "/docs"}

@app.get("/api-docs", response_class=PlainTextResponse)
def get_api_docs():
    """
    Serve API documentation as plain text for ChatGPT and other AI assistants.
    This endpoint returns a human-readable markdown document.
    """
    from pathlib import Path
    
    docs_path = Path(__file__).parent / "static" / "api-docs.md"
    if docs_path.exists():
        return PlainTextResponse(docs_path.read_text())
    else:
        return PlainTextResponse("API documentation not found", status_code=404)

@app.get("/health")
def health_check():
    """Comprehensive health check endpoint"""
    from app.db.session import engine
    from sqlalchemy import text
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "api": "ok",
            "database": "unknown"
        }
    }
    
    # Check database
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            health_status["checks"]["database"] = "ok"
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["checks"]["database"] = f"error: {str(e)}"
        logger.error(f"Database health check failed: {e}")
    
    return health_status

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

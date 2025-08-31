# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, external, health, parts, products, stores, tags, search, logs
from app.logging_config import configure_logging, LoggingMiddleware, get_logger

# Configure logging first
configure_logging()
logger = get_logger("main")

# Load local .env if present (useful for local development)
if os.getenv("RAILWAY_ENVIRONMENT") is None:
    from dotenv import load_dotenv

    load_dotenv()

app = FastAPI(title="Partle API")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

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
app.include_router(health.router, prefix="/v1")


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"status": "ok", "version": "v1", "docs": "/docs"}

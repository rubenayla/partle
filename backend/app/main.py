# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, external, parts, products, stores, tags

# Load local .env if present (useful for local development)
if os.getenv("RAILWAY_ENVIRONMENT") is None:
    from dotenv import load_dotenv

    load_dotenv()

app = FastAPI(title="Partle API")

# CORS (must be added before routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://partle.vercel.app", "http://localhost:5173"],
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


@app.get("/")
def root():
    return {"status": "ok", "version": "v1", "docs": "/docs"}

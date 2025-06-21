# backend/app/main.py
from app.api.v1 import auth, external, parts, products, stores
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Partle API")

# All under /v1/…
app.include_router(parts.router, prefix="/v1/parts", tags=["Parts"])
app.include_router(stores.router, prefix="/v1/stores", tags=["Stores"])
app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/v1/products", tags=["Products"])
app.include_router(external.router, prefix="/v1/external", tags=["External"])

# CORS (frontend port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://partle.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "version": "v1", "docs": "/docs"}

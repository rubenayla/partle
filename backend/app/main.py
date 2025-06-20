# backend/app/main.py
from fastapi import FastAPI
from app.api.v1 import parts, stores, auth, products
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Partle API")

# All under /v1/…
app.include_router(parts.router, prefix="/v1/parts", tags=["Parts"])
app.include_router(stores.router, prefix="/v1/stores", tags=["Stores"])
app.include_router(auth.router, prefix="/v1/auth", tags=["Auth"])
app.include_router(products.router, prefix="/v1/products", tags=["Products"])

# CORS (frontend port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "version": "v1", "docs": "/docs"}

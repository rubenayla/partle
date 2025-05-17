from fastapi import FastAPI
from app.api.v1 import parts, stores
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Partle API")

app.include_router(parts.router, prefix="/v1/parts", tags=["Parts"])
app.include_router(stores.router, prefix="/v1/stores", tags=["Stores"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

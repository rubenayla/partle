# backend/app/schemas/product.py
from decimal import Decimal
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class ProductIn(BaseModel):
    """Fields a client may send when creating a product."""
    store_id: Optional[int] = None        # nullable → orphan products allowed
    name: str
    spec: Optional[str] = None
    price: Optional[Decimal] = None       # Decimal ↔ SQLAlchemy Numeric
    url: Optional[HttpUrl] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)  # pydantic-v2 replacement for orm_mode


class ProductUpdate(ProductIn):
    """PATCH body – every field becomes optional."""
    name: Optional[str] = None


from app.schemas.tag import Tag


class ProductOut(ProductIn):
    """What the API returns."""
    id: int
    updated_at: datetime
    updated_by_id: Optional[int] = None
    tags: list[Tag] = []


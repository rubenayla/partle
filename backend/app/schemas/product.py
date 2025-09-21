# backend/app/schemas/product.py
from decimal import Decimal
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class ProductIn(BaseModel):
    """Fields a client may send when creating a product."""
    store_id: Optional[int] = None        # nullable → orphan products allowed
    name: str
    sku: Optional[str] = None             # Stock Keeping Unit - unique per store
    spec: Optional[str] = None
    price: Optional[Decimal] = None       # Decimal ↔ SQLAlchemy Numeric
    currency: Optional[str] = '€'         # Free text currency field, defaults to €
    url: Optional[HttpUrl] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    description: Optional[str] = None
    image_filename: Optional[str] = None
    image_content_type: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)  # pydantic-v2 replacement for orm_mode


class ProductUpdate(ProductIn):
    """PATCH body – every field becomes optional."""
    name: Optional[str] = None


from app.schemas.tag import Tag
from typing import TYPE_CHECKING

# Minimal user info to include with products
class UserBasic(BaseModel):
    """Basic user info for product creator display."""
    id: int
    username: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class ProductOut(ProductIn):
    """What the API returns."""
    id: int
    created_at: datetime
    updated_at: datetime
    updated_by_id: Optional[int] = None
    creator_id: Optional[int] = None
    creator: Optional[UserBasic] = None
    image_filename: Optional[str] = None
    image_content_type: Optional[str] = None
    tags: list[Tag] = []


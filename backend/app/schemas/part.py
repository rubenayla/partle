from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str
    spec: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    description: Optional[str] = None
    store_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel, HttpUrl
from typing import Optional

class ProductIn(BaseModel):
    store_id: int
    name: str
    spec: Optional[str] = None
    price: Optional[float] = None
    url: Optional[HttpUrl] = None

class ProductOut(ProductIn):
    id: int

    class Config:
        orm_mode = True

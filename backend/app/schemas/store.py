from pydantic import BaseModel, Field
from typing import Optional, Literal


class StoreBase(BaseModel):
    name: str
    type: Literal["physical", "online"]
    address: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    homepage: Optional[str] = None


class StoreCreate(StoreBase):
    pass


class StoreRead(StoreBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from typing import Optional, Literal
from app.schemas.tag import Tag


class StoreBase(BaseModel):
    name: str
    type: Literal["physical", "online", "chain"]
    address: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    homepage: Optional[str] = None


class StoreCreate(StoreBase):
    pass


class StoreRead(StoreBase):
    id: int
    owner_id: Optional[int] = None
    tags: list[Tag] = []
    logo_filename: Optional[str] = None
    logo_content_type: Optional[str] = None

    class Config:
        from_attributes = True

# backend/app/schemas/tag.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TagBase(BaseModel):
    name: str
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

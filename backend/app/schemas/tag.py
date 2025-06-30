# backend/app/schemas/tag.py
from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

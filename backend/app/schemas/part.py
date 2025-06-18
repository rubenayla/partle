from pydantic import BaseModel


class PartBase(BaseModel):
    name: str
    sku: str | None = None
    stock: int
    price: float | None = None
    store_id: int


class PartCreate(PartBase):
    pass


class PartOut(PartBase):
    id: int

    class Config:
        orm_mode = True

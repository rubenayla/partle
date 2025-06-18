from pydantic import BaseModel


class StoreBase(BaseModel):
    name: str
    lat: float
    lon: float


class StoreCreate(StoreBase):
    pass


class StoreOut(StoreBase):
    id: int

    class Config:
        orm_mode = True

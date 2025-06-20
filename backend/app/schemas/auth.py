# backend/app/schemas/auth.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class EmailOnly(BaseModel):
    email: EmailStr


class FidoFinish(BaseModel):
    email: EmailStr
    credential: dict

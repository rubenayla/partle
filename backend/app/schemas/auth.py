# backend/app/schemas/auth.py
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str | None = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class EmailOnly(BaseModel):
    email: EmailStr


# class FidoFinish(BaseModel):
#     email: EmailStr
#     credential: dict


class RegisterInput(BaseModel):
    email: EmailStr
    password: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class SetUsername(BaseModel):
    username: str

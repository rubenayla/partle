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


class FidoLoginBegin(BaseModel):
    email: EmailStr


class FidoLoginFinish(BaseModel):
    email: EmailStr
    credential_id: bytes
    client_data_json: bytes
    authenticator_data: bytes
    signature: bytes


class FidoRegisterFinish(BaseModel):
    client_data_json: bytes
    attestation_object: bytes

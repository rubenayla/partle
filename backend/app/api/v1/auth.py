# backend/app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.security import get_current_user
from app.db.session import SessionLocal
from app.db.models import User, Credential
from app.schemas import auth as schema
from fido2.server import Fido2Server
from fido2.webauthn import (
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    AttestedCredentialData,
)
from fido2 import cbor
from fido2.cose import CoseKey

fido_server = Fido2Server(PublicKeyCredentialRpEntity(name="Partle", id="localhost"))
reg_state: dict[str, any] = {}
auth_state: dict[str, any] = {}
from app.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter()


# ───── DB Dependency ────────────────────────────────────────────
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ───── Endpoints ────────────────────────────────────────────────
@router.post("/register", response_model=schema.UserRead)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schema.Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=form.username).first()
    if not user or not user.password_hash or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schema.UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/fido/register/begin", response_model=dict)
def fido_register_begin(payload: schema.EmailOnly, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        user = User(email=payload.email)
        db.add(user)
        db.commit()
        db.refresh(user)
    user_entity = PublicKeyCredentialUserEntity(name=user.email, id=str(user.id).encode())
    options, state = fido_server.register_begin(user_entity)
    reg_state[user.email] = state
    return options["publicKey"]


@router.post("/fido/register/complete", response_model=schema.Token)
def fido_register_complete(payload: schema.FidoFinish, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or user.email not in reg_state:
        raise HTTPException(status_code=400, detail="Registration not started")
    state = reg_state.pop(user.email)
    auth_data = fido_server.register_complete(state, payload.credential)
    cred = Credential(
        credential_id=auth_data.credential_data.credential_id,
        public_key=cbor.encode(auth_data.credential_data.public_key),
        sign_count=auth_data.counter,
        user_id=user.id,
    )
    db.add(cred)
    db.commit()
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/fido/login/begin", response_model=dict)
def fido_login_begin(payload: schema.EmailOnly, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    creds = []
    for cred in user.credentials:
        key = CoseKey.parse(cbor.decode(cred.public_key))
        creds.append(AttestedCredentialData.create(b"\x00" * 16, cred.credential_id, key))
    options, state = fido_server.authenticate_begin(creds)
    auth_state[user.email] = state
    return options["publicKey"]


@router.post("/fido/login/complete", response_model=schema.Token)
def fido_login_complete(payload: schema.FidoFinish, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or user.email not in auth_state:
        raise HTTPException(status_code=400, detail="Login not started")
    state = auth_state.pop(user.email)
    creds = []
    for cred in user.credentials:
        key = CoseKey.parse(cbor.decode(cred.public_key))
        creds.append(AttestedCredentialData.create(b"\x00" * 16, cred.credential_id, key))
    fido_server.authenticate_complete(state, creds, payload.credential)
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

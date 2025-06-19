# backend/app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.security import get_current_user
from app.db.session import SessionLocal
from app.db.models import User
from app.schemas import auth as schema
from app.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
)
from fido2.server import Fido2Server
from fido2.webauthn import (
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    PublicKeyCredentialDescriptor,
)
from dataclasses import asdict
from fido2.utils import websafe_encode

router = APIRouter()
rp = PublicKeyCredentialRpEntity("localhost", "Partle")
fido_server = Fido2Server(rp)
fido_states: dict[str, dict] = {}


def _encode(obj):
    if isinstance(obj, bytes):
        return websafe_encode(obj)
    if hasattr(obj, "value") and not isinstance(obj, bytes):
        return obj.value
    if isinstance(obj, dict):
        return {k: _encode(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_encode(v) for v in obj]
    return obj


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
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/fido/login/begin")
def fido_login_begin(payload: schema.FidoLoginBegin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or not user.fido_id:
        raise HTTPException(status_code=404, detail="No credential")

    descriptor = PublicKeyCredentialDescriptor(id=user.fido_id, type="public-key")
    options, state = fido_server.authenticate_begin([descriptor])
    fido_states[payload.email] = state
    return _encode(asdict(options))


@router.post("/fido/login/finish", response_model=schema.Token)
def fido_login_finish(payload: schema.FidoLoginFinish, db: Session = Depends(get_db)):
    state = fido_states.pop(payload.email, None)
    if not state:
        raise HTTPException(status_code=400, detail="No login in progress")
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or not user.fido_id:
        raise HTTPException(status_code=404, detail="No credential")
    descriptor = PublicKeyCredentialDescriptor(id=user.fido_id, type="public-key")
    fido_server.authenticate_complete(
        state,
        [descriptor],
        payload.credential_id,
        payload.client_data_json,
        payload.authenticator_data,
        payload.signature,
    )
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schema.UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/fido/register/begin")
def fido_register_begin(current_user: User = Depends(get_current_user)):
    user_entity = PublicKeyCredentialUserEntity(
        id=str(current_user.id).encode(),
        name=current_user.email,
        display_name=current_user.email,
    )
    options, state = fido_server.register_begin(user_entity)
    fido_states[str(current_user.id)] = state
    return _encode(asdict(options))


@router.post("/fido/register/finish")
def fido_register_finish(
    payload: schema.FidoRegisterFinish,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    state = fido_states.pop(str(current_user.id), None)
    if not state:
        raise HTTPException(status_code=400, detail="No registration in progress")
    auth_data = fido_server.register_complete(
        state, payload.client_data_json, payload.attestation_object
    )
    current_user.fido_id = auth_data.credential_data.credential_id
    current_user.fido_pubkey = auth_data.credential_data.public_key
    db.add(current_user)
    db.commit()
    return {"status": "ok"}

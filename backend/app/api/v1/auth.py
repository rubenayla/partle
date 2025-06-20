# backend/app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import User, Credential  # noqa: F401 (Credential used elsewhere)
from app.schemas import auth as schema
from app.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_reset_token,
    send_reset_email,
)
from app.auth.security import get_current_user

# ----------  FIDO (unchanged)  ------------------------------------------------
from fido2.server import Fido2Server
from fido2.webauthn import (
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialType,
    AuthenticationResponse,
    AttestedCredentialData,
    Aaguid,
)
from fido2 import cbor

fido_server = Fido2Server(PublicKeyCredentialRpEntity(name="Partle", id="localhost"))
reg_state: dict[str, any] = {}
auth_state: dict[str, any] = {}

# ------------------------------------------------------------------------------

router = APIRouter()


# ─── DB Dependency ────────────────────────────────────────────────────────────
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── Register (create or overwrite password) ─────────────────────────────────
@router.post("/register")
def register(data: schema.RegisterInput, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()

    if user:
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(email=data.email, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    return {"status": "ok"}


# ─── Login (OAuth2 form) ─────────────────────────────────────────────────────
@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(email=form.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# ─── Password-reset request ──────────────────────────────────────────────────
@router.post("/request-password-reset", status_code=202)
async def request_password_reset(
    payload: schema.EmailOnly,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(email=payload.email).first()
    if user:
        token = create_reset_token(user)
        background_tasks.add_task(send_reset_email, user.email, token)

    return {"status": "ok"}


# ─── Get current user ───────────────────────────────────────────────────────
@router.get("/me", response_model=schema.UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


# ─── FIDO2 Registration -----------------------------------------------------
@router.post("/fido/register/begin")
def fido_register_begin(payload: schema.EmailOnly, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        user = User(email=payload.email)
        db.add(user)
        db.commit()
        db.refresh(user)

    existing = [
        PublicKeyCredentialDescriptor(
            type=PublicKeyCredentialType.PUBLIC_KEY,
            id=c.credential_id,
        )
        for c in user.credentials
    ]
    options, state = fido_server.register_begin(
        {
            "id": str(user.id).encode(),
            "name": user.email,
            "displayName": user.email,
        },
        credentials=existing or None,
    )
    reg_state[payload.email] = state
    return options


@router.post("/fido/register/complete", response_model=schema.Token)
def fido_register_complete(
    payload: schema.FidoFinish, db: Session = Depends(get_db)
):
    state = reg_state.pop(payload.email, None)
    if state is None:
        raise HTTPException(status_code=400, detail="No registration in progress")

    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    auth_data = fido_server.register_complete(state, payload.credential)
    cred_data = auth_data.credential_data
    assert cred_data is not None

    cred = Credential(
        credential_id=cred_data.credential_id,
        public_key=cbor.encode(cred_data.public_key),
        sign_count=auth_data.counter,
        user=user,
    )
    db.add(cred)
    db.commit()

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# ─── FIDO2 Authentication ----------------------------------------------------
@router.post("/fido/login/begin")
def fido_login_begin(payload: schema.EmailOnly, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()
    if not user or not user.credentials:
        raise HTTPException(status_code=404, detail="User not found")

    allowed = [
        PublicKeyCredentialDescriptor(
            type=PublicKeyCredentialType.PUBLIC_KEY,
            id=c.credential_id,
        )
        for c in user.credentials
    ]
    options, state = fido_server.authenticate_begin(allowed)
    auth_state[payload.email] = state
    return options


@router.post("/fido/login/complete", response_model=schema.Token)
def fido_login_complete(payload: schema.FidoFinish, db: Session = Depends(get_db)):
    state = auth_state.pop(payload.email, None)
    if state is None:
        raise HTTPException(status_code=400, detail="No authentication in progress")

    user = db.query(User).filter_by(email=payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_creds = {c.credential_id: c for c in user.credentials}
    creds = [
        AttestedCredentialData.create(
            Aaguid(b"\x00" * 16),
            c.credential_id,
            cbor.decode(c.public_key),
        )
        for c in db_creds.values()
    ]

    fido_server.authenticate_complete(state, creds, payload.credential)

    auth_resp = AuthenticationResponse.from_dict(payload.credential)
    counter = auth_resp.response.authenticator_data.counter
    cred_id = auth_resp.raw_id
    stored = db_creds.get(cred_id)
    if stored is None:
        raise HTTPException(status_code=400, detail="Unknown credential")
    if counter <= stored.sign_count:
        raise HTTPException(status_code=400, detail="Invalid sign count")
    stored.sign_count = counter
    db.commit()

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

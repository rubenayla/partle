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

# ----------  FIDO (unchanged)  ------------------------------------------------
from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity

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

    if not user:
        user = User(email=data.email, password_hash=hash_password(data.password))
        db.add(user)
    else:
        user.password_hash = hash_password(data.password)

    db.commit()
    return {"status": "ok"}


# ─── Login (OAuth2 form) ─────────────────────────────────────────────────────
@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(email=form.username).first()

    if not user or not verify_password(form.password, user.password_hash):
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

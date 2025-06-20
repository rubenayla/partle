# backend/app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import User, Product
from app.schemas import auth as schema
from app.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_reset_token,
    send_reset_email,
)
from app.auth.security import get_current_user

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


@router.delete("/account", status_code=204)
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete the current user's account."""
    db.query(Product).filter_by(creator_id=current_user.id).update({Product.creator_id: None})
    db.query(User).filter_by(id=current_user.id).delete()
    db.commit()

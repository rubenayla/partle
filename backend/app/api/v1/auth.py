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
    verify_reset_token,
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


# ─── Login (OAuth2 form) - Auto-registers new users ─────────────────────────
@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(email=form.username).first()

    if not user:
        # Auto-register new user with provided password
        user = User(email=form.username, password_hash=hash_password(form.password))
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Existing user - verify password
        if not verify_password(form.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token, 
        "token_type": "bearer",
        "needs_username": user.username is None
    }


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


    return {"status": "ok"}


# ─── Password-reset confirmation ─────────────────────────────────────────────
@router.post("/reset-password", status_code=200)
def reset_password(
    data: schema.PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    email = verify_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(data.new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"status": "ok"}


# ─── Get current user ───────────────────────────────────────────────────────
@router.get("/me", response_model=schema.UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/set-username")
def set_username(
    payload: schema.SetUsername,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set username for the current user (one-time only)."""
    if current_user.username is not None:
        raise HTTPException(status_code=400, detail="Username already set")
    
    # Check if username is already taken
    existing = db.query(User).filter_by(username=payload.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")
    
    # Validate username (alphanumeric, underscore, dash, 3-20 chars)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]{3,20}$', payload.username):
        raise HTTPException(
            status_code=400, 
            detail="Username must be 3-20 characters, alphanumeric, underscore or dash only"
        )
    
    current_user.username = payload.username
    db.commit()
    return {"status": "ok", "username": current_user.username}


@router.delete("/account", status_code=204)
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete the current user's account."""
    db.query(Product).filter_by(creator_id=current_user.id).update({Product.creator_id: None})
    db.query(User).filter_by(id=current_user.id).delete()
    db.commit()


# ─── Logout ───────────────────────────────────────────────────────────────────
@router.post("/logout", status_code=204)
def logout(current_user: User = Depends(get_current_user)):
    """Placeholder endpoint for logging out JWT-based sessions."""
    return None


# ─── Change Password ─────────────────────────────────────────────────────────
@router.post("/change-password", status_code=200)
def change_password(
    data: schema.PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect current password")

    current_user.password_hash = hash_password(data.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"status": "ok"}

import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from itsdangerous import URLSafeTimedSerializer

# ─── Auth basics ──────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ─── Password-reset helpers ───────────────────────────────────────────────
_serializer = URLSafeTimedSerializer(SECRET_KEY, salt="pwd-reset")


def create_reset_token(user) -> str:
    """
    Return a time-signed token containing the user’s e-mail.
    Valid for one hour (check in verify_reset_token).
    """
    return _serializer.dumps(user.email)


def verify_reset_token(token: str, max_age: int = 3600) -> str | None:
    """
    Return the e-mail if token valid & unexpired, else None.
    """
    try:
        return _serializer.loads(token, max_age=max_age)
    except Exception:  # itsdangerous.BadSignature / .SignatureExpired
        return None


import smtplib
from email.message import EmailMessage


def send_reset_email(to_email: str, token: str) -> None:
    link = f"https://partle.com/reset?token={token}"
    msg = EmailMessage()
    msg["Subject"] = "Reset your Partle password"
    msg["From"] = os.environ.get("SMTP_USERNAME")
    msg["To"] = to_email
    msg.set_content(f"Click here to reset your password:\n{link}")

    with smtplib.SMTP_SSL(os.environ.get("SMTP_HOST"), os.environ.get("SMTP_PORT")) as smtp:
        smtp.login(os.environ.get("SMTP_USERNAME"), os.environ.get("SMTP_PASSWORD"))
        smtp.send_message(msg)

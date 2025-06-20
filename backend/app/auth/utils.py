from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from itsdangerous import URLSafeTimedSerializer

# ─── Auth basics ──────────────────────────────────────────────────────────
SECRET_KEY = "super-secret"  # TODO move to env / settings
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


def send_reset_email(to_email: str, token: str) -> None:
    """
    Dev helper: prints reset link to console.  Replace with real mailer.
    """
    link = f"https://partle.com/reset?token={token}"
    print(f"\n[RESET] To: {to_email}\n      → {link}\n")


# TODO VERCEL OR CLOUDFLARE FOR THIS
# import smtplib
# from email.message import EmailMessage

# def send_reset_email(to_email: str, token: str) -> None:
#     link = f"https://partle.com/reset?token={token}"
#     msg = EmailMessage()
#     msg["Subject"] = "Reset your Partle password"
#     msg["From"] = "no-reply@partle.com"
#     msg["To"] = to_email
#     msg.set_content(f"Click here to reset your password:\n{link}")

#     # You need a real SMTP service here
#     with smtplib.SMTP_SSL("smtp.mailprovider.com", 465) as smtp:
#         smtp.login("your-user", "your-pass")
#         smtp.send_message(msg)

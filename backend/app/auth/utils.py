import os
from datetime import datetime, timedelta, UTC
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
    expire = datetime.now(UTC) + (
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


import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)


def send_reset_email(to_email: str, token: str) -> None:
    """Send password reset email via Cloudflare Worker"""
    worker_url = os.environ.get("CLOUDFLARE_WORKER_URL")
    worker_api_key = os.environ.get("CLOUDFLARE_WORKER_API_KEY")
    
    if not worker_url or not worker_api_key:
        logger.error("Missing Cloudflare Worker configuration")
        raise Exception("Missing Cloudflare Worker configuration")
    
    payload = {
        "to_email": to_email,
        "token": token,
        "api_key": worker_api_key
    }
    
    logger.info(f"Sending password reset email to: {to_email}")
    logger.debug(f"Worker URL: {worker_url}")
    logger.debug(f"Token (first 20 chars): {token[:20]}...")
    
    try:
        response = requests.post(worker_url, json=payload, timeout=10)
        logger.info(f"Cloudflare Worker response: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        
        if response.status_code != 200:
            logger.error(f"Failed to send email. Status: {response.status_code}, Body: {response.text}")
            raise Exception(f"Failed to send email: {response.text}")
        
        logger.info(f"Password reset email sent successfully to {to_email}")
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout sending email to {to_email} - Cloudflare Worker didn't respond in 10s")
        raise Exception("Email service timeout - please try again")
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error sending email to {to_email}: {e}")
        raise Exception(f"Network error sending email: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error sending email to {to_email}: {e}")
        raise

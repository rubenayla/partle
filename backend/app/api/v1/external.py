"""External API endpoints."""

from collections.abc import Generator

from app.db.models import Product, Store, User
from app.db.session import SessionLocal
from app.schemas import product as schema
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

# Hardcoded mapping of API keys to user IDs
API_KEYS: dict[str, int] = {"abc123": 1}


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_external_user(
    api_key: str | None = Header(None, alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> User:
    if not api_key or api_key not in API_KEYS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")
    user = db.get(User, API_KEYS[api_key])
    if not user or not user.stores:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "User not allowed")
    return user


@router.post(
    "/products",
    response_model=schema.ProductOut,
    status_code=201,
    summary="Create product via API key",
)
def create_product_external(
    payload: schema.ProductIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_external_user),
):
    if payload.store_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "store_id required")
    store = db.get(Store, payload.store_id)
    if not store or store.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden")

    existing = (
        db.query(Product)
        .filter_by(name=payload.name, store_id=payload.store_id)
        .first()
    )
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Product already exists")

    product = Product(**payload.model_dump(), creator_id=user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# backend/app/api/v1/products.py
from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Product, User
from app.db.session import SessionLocal
from app.schemas import product as schema
from app.auth.security import get_current_user

router = APIRouter()


# ───────────────────────────────────────────
# Shared dependency
# ───────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ───────────────────────────────────────────
# CRUD endpoints
# ───────────────────────────────────────────
@router.get("/", response_model=list[schema.ProductOut])
def list_products(
    store_id: int | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Product)
    if store_id is not None:
        q = q.filter(Product.store_id == store_id)
    return q.all()


@router.get("/store/{store_id}", response_model=list[schema.ProductOut])
def list_products_by_store(store_id: int, db: Session = Depends(get_db)):
    """List products for a specific store."""
    return db.query(Product).filter(Product.store_id == store_id).all()


# TODO HOW TO UPDATE PRODUCT
@router.post("/", response_model=schema.ProductOut, status_code=201)
def create_product(
    payload: schema.ProductIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = (
        db.query(Product)
        .filter_by(name=payload.name, store_id=payload.store_id)
        .first()
    )
    if existing:
        raise HTTPException(409, "Product already exists")

    product = Product(
        **payload.model_dump(),
        creator_id=current_user.id,
        updated_by_id=current_user.id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=schema.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.patch("/{product_id}", response_model=schema.ProductOut)
def update_product(
    product_id: int,
    payload: schema.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    product.updated_by_id = current_user.id

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    db.delete(product)
    db.commit()

# backend/app/api/v1/products.py
from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.models import Product, User, Tag
from app.schemas import product as schema
from app.auth.security import get_current_user
from app.api.deps import get_db

router = APIRouter()


# ───────────────────────────────────────────
# CRUD endpoints
# ───────────────────────────────────────────
@router.get("/", response_model=list[schema.ProductOut])
def list_products(
    store_id: int | None = None,
    tags: str = Query(""),
    db: Session = Depends(get_db),
):
    q = db.query(Product)
    if store_id is not None:
        q = q.filter(Product.store_id == store_id)
    if tags:
        tag_ids = [int(tag_id) for tag_id in tags.split(',') if tag_id]
        q = q.filter(Product.tags.any(Tag.id.in_(tag_ids)))
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


@router.post("/{product_id}/tags/{tag_id}", response_model=schema.ProductOut, status_code=201)
def add_tag_to_product(
    product_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    product.tags.append(tag)
    db.commit()
    db.refresh(product)
    return product

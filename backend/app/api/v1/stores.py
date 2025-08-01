# backend/app/api/v1/stores.py
"""Stores API router.

Endpoints:
- `GET /v1/stores/`      → list stores (public)
- `GET /v1/stores`        → same as above (fallback without trailing slash)
- `POST /v1/stores/`      → create store (auth required)
- `GET /v1/stores/{id}`   → get single store
- `DELETE /v1/stores/{id}`→ delete store
"""
from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.auth.security import get_current_user
from app.db.models import Store, User, Tag
from app.schemas import store as schema
from app.api.deps import get_db

router = APIRouter(tags=["Stores"])

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@router.get("/", response_model=list[schema.StoreRead])
def list_stores(
    q: str | None = None,
    tags: str | None = None,
    sort_by: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Return stores with optional search, filtering and pagination."""
    query = db.query(Store)

    if q:
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Store.name.ilike(search_term),
                Store.address.ilike(search_term),
                Store.homepage.ilike(search_term)
            )
        )

    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        if tag_list:
            query = query.join(Store.tags).filter(Tag.name.in_(tag_list))

    if sort_by == "created_at":
        query = query.order_by(Store.created_at.desc())
    elif sort_by == "created_at_asc":
        query = query.order_by(Store.created_at.asc())
    elif sort_by == "random":
        query = query.order_by(func.random())

    return query.offset(offset).limit(limit).all()


# Allow `/v1/stores` (without the trailing slash) to work too.
# `include_in_schema=False` prevents duplicate docs entries.
@router.get("", response_model=list[schema.StoreRead], include_in_schema=False)
def list_stores_alt(
    q: str | None = None,
    tags: str | None = None,
    sort_by: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return list_stores(q=q, tags=tags, sort_by=sort_by, limit=limit, offset=offset, db=db)


@router.post("/", response_model=schema.StoreRead, status_code=status.HTTP_201_CREATED)
def create_store(
    payload: schema.StoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new store owned by the authenticated user."""
    new_store = Store(**payload.model_dump(), owner_id=current_user.id)
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    return new_store


@router.get("/{store_id}", response_model=schema.StoreRead)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """Retrieve a single store by *id*."""
    store = db.get(Store, store_id)  # SQLAlchemy 1.4+ style
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    return store


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    """Delete a store by *id*."""
    store = db.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    db.delete(store)
    db.commit()


@router.post("/{store_id}/tags/{tag_id}", response_model=schema.StoreRead, status_code=201)
def add_tag_to_store(
    store_id: int,
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a tag to a store."""
    store = db.get(Store, store_id)
    if not store:
        raise HTTPException(404, "Store not found")

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    store.tags.append(tag)
    db.commit()
    db.refresh(store)
    return store
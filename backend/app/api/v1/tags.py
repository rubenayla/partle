# backend/app/api/v1/tags.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tag import Tag, TagCreate
from app.db import models
from app.api.deps import get_db

router = APIRouter()


@router.post("/", response_model=Tag, status_code=201)
def create_tag(
    *,
    db: Session = Depends(get_db),
    tag_in: TagCreate,
) -> models.Tag:
    """
    Create new tag.
    """
    tag = db.query(models.Tag).filter(models.Tag.name == tag_in.name).first()
    if tag:
        raise HTTPException(
            status_code=400,
            detail="A tag with this name already exists.",
        )
    tag = models.Tag(name=tag_in.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@router.get("/", response_model=list[Tag])
def read_tags(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[models.Tag]:
    """
    Retrieve tags.
    """
    tags = db.query(models.Tag).offset(skip).limit(limit).all()
    return tags


@router.post("/{tag_id}/stores/{store_id}", response_model=Tag)
def add_tag_to_store(
    *,
    db: Session = Depends(get_db),
    tag_id: int,
    store_id: int,
) -> models.Tag:
    """
    Add a tag to a store.
    """
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    store.tags.append(tag)
    db.commit()
    db.refresh(tag)
    return tag

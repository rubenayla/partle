# backend/app/api/v1/tags.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tag import Tag, TagCreate
from app.db import models
from app.api.deps import get_db
from app.auth.security import get_current_user
from app.db.models import User

router = APIRouter()


@router.post("/", response_model=Tag, status_code=201)
def create_tag(
    *,
    db: Session = Depends(get_db),
    tag_in: TagCreate,
    current_user: User = Depends(get_current_user),
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


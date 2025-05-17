from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
from app.schemas.part import PartCreate, PartOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[PartOut])
def get_parts(db: Session = Depends(get_db)):
    return db.query(models.Part).all()

@router.post("/", response_model=PartOut)
def add_part(part: PartCreate, db: Session = Depends(get_db)):
    db_part = models.Part(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

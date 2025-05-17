from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db import models
from app.schemas.store import StoreCreate, StoreOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[StoreOut])
def get_stores(db: Session = Depends(get_db)):
    return db.query(models.Store).all()

@router.post("/", response_model=StoreOut)
def add_store(store: StoreCreate, db: Session = Depends(get_db)):
    db_store = models.Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

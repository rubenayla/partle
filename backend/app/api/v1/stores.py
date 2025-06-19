from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Store
from app.schemas import store as schema
from collections.abc import Generator

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/", response_model=list[schema.StoreRead])
def list_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()


@router.post("/", response_model=schema.StoreRead, status_code=201)
def create_store(payload: schema.StoreCreate, db: Session = Depends(get_db)):
    new_store = Store(**payload.model_dump())
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    return new_store


@router.get("/{store_id}", response_model=schema.StoreRead)
def get_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).get(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.delete("/{store_id}", status_code=204)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).get(store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(store)
    db.commit()

import os
import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Store, StoreType

def add_bricodepot_store():
    db: Session = SessionLocal()
    try:
        # Check if the store already exists to prevent duplicates
        existing_store = db.query(Store).filter(Store.name == "Bricodepot (Chain)").first()
        if existing_store:
            print("Bricodepot (Chain) store already exists.")
            return

        new_store = Store(
            name="Bricodepot (Chain)",
            type=StoreType.CHAIN,
            address="N/A",
            homepage="https://www.bricodepot.es/"
        )
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        print(f"Successfully added Bricodepot (Chain) store with ID: {new_store.id}")
    except Exception as e:
        db.rollback()
        print(f"Error adding Bricodepot (Chain) store: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Add backend directory to Python path to allow imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
    add_bricodepot_store()

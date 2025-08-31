#!/usr/bin/env python3
"""
Check if Mengual store exists and create it if needed
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, '/home/rubenayla/repos/partle/backend')

try:
    from app.db.models import Store
except ImportError:
    print("Could not import models")
    sys.exit(1)

def main():
    # Use the same database URL as the scraper
    DATABASE_URL = "postgresql://postgres:partl3p4ss@localhost:5432/partle"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = SessionLocal()
    
    try:
        # Check if Mengual store exists
        mengual_store = db.query(Store).filter(Store.id == 4070).first()
        if mengual_store:
            print(f"Store exists: {mengual_store.name} (ID: {mengual_store.id})")
        else:
            print("Store 4070 not found - creating it...")
            
            # Create Mengual store
            from app.db.models import StoreType
            new_store = Store(
                id=4070,
                name="Mengual",
                type=StoreType.online,  # Correct field name is 'type'
                homepage="https://www.mengual.com",  # Correct field name is 'homepage'
            )
            
            db.add(new_store)
            db.commit()
            print(f"Created store: {new_store.name} (ID: {new_store.id})")

        # Show all stores
        stores = db.query(Store).all()
        print(f"\nTotal stores: {len(stores)}")
        for store in stores:
            print(f"  {store.id}: {store.name} ({store.type.value if store.type else 'unknown'})")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()
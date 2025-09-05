#!/usr/bin/env python3
"""
Create multiple test stores for bulk product generation
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from root .env
root_env = Path(__file__).parent.parent / '.env'
load_dotenv(root_env, override=True)

# Add the backend directory to Python path
sys.path.insert(0, '/home/rubenayla/repos/partle/backend')

try:
    from app.db.models import Store, StoreType
except ImportError:
    print("Could not import models")
    sys.exit(1)

def main():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("Error: DATABASE_URL environment variable is required")
        sys.exit(1)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = SessionLocal()
    
    try:
        # Create multiple test stores for bulk scraping
        test_stores = [
            (5001, "ToolMaster Pro", "online", "https://example.com/toolmaster"),
            (5002, "Hardware World", "online", "https://example.com/hardwareworld"),
            (5003, "Construction Central", "online", "https://example.com/constructioncentral"),
            (5004, "Builder's Paradise", "online", "https://example.com/buildersparadise"),
            (5005, "Industrial Supply Co", "online", "https://example.com/industrialsupply"),
            (5006, "Home Repair Hub", "online", "https://example.com/homerepairhub"),
        ]
        
        for store_id, name, store_type, homepage in test_stores:
            # Check if store exists
            existing = db.query(Store).filter(Store.id == store_id).first()
            if not existing:
                new_store = Store(
                    id=store_id,
                    name=name,
                    type=StoreType.online,
                    homepage=homepage
                )
                db.add(new_store)
                print(f"Created store: {name} (ID: {store_id})")
            else:
                print(f"Store already exists: {name} (ID: {store_id})")
        
        db.commit()
        print("All test stores created successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()
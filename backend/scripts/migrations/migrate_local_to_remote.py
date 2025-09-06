#!/usr/bin/env python3
"""
Script to migrate Rationalstock products from local database to remote database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Product, Store, StoreType

# Database URLs
LOCAL_DB_URL = "postgresql://postgres:partl3p4ss@localhost:5432/partle"
REMOTE_DB_URL = "postgresql://partle_user:v4zxTX7VN2Ljynlhon1fLg==@91.98.68.236:5432/partle"

def migrate_products():
    # Connect to both databases
    local_engine = create_engine(LOCAL_DB_URL, echo=False)
    remote_engine = create_engine(REMOTE_DB_URL, echo=False)
    
    LocalSession = sessionmaker(bind=local_engine)
    RemoteSession = sessionmaker(bind=remote_engine)
    
    local_db = LocalSession()
    remote_db = RemoteSession()
    
    try:
        # Get Rationalstock products from local database
        local_products = local_db.query(Product).filter(Product.store_id == 4066).all()
        print(f"Found {len(local_products)} Rationalstock products in local database")
        
        # Check if Rationalstock store exists in remote
        remote_store = remote_db.query(Store).filter(Store.id == 4066).first()
        if not remote_store:
            print("Creating Rationalstock store in remote database...")
            remote_store = Store(
                id=4066,
                name='Rationalstock',
                type=StoreType.online,
                homepage='https://www.rationalstock.es/'
            )
            remote_db.add(remote_store)
            remote_db.flush()
        
        migrated_count = 0
        skipped_count = 0
        
        for local_product in local_products:
            # Check if product already exists in remote (by URL to avoid duplicates)
            existing = remote_db.query(Product).filter(
                Product.url == local_product.url,
                Product.store_id == 4066
            ).first()
            
            if existing:
                print(f"Skipping duplicate: {local_product.name}")
                skipped_count += 1
                continue
            
            # Create new product in remote database
            remote_product = Product(
                name=local_product.name,
                spec=local_product.spec,
                price=local_product.price,
                url=local_product.url,
                lat=local_product.lat,
                lon=local_product.lon,
                description=local_product.description,
                image_url=local_product.image_url,
                store_id=4066,
                creator_id=local_product.creator_id,
                created_at=local_product.created_at,
                updated_at=local_product.updated_at,
                updated_by_id=local_product.updated_by_id
            )
            
            remote_db.add(remote_product)
            migrated_count += 1
            print(f"Migrated: {local_product.name}")
        
        # Commit all changes
        remote_db.commit()
        
        print(f"\nMigration completed:")
        print(f"  - Migrated: {migrated_count} products")
        print(f"  - Skipped (duplicates): {skipped_count} products")
        print(f"  - Total in remote: {remote_db.query(Product).filter(Product.store_id == 4066).count()} products")
        
    except Exception as e:
        remote_db.rollback()
        print(f"Error during migration: {e}")
        raise
    finally:
        local_db.close()
        remote_db.close()

if __name__ == "__main__":
    migrate_products()
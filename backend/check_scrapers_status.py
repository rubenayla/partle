#!/usr/bin/env python3
"""
Check all scrapers and database status
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, '/home/rubenayla/repos/partle/backend')

try:
    from app.db.models import Store, Product
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
        print("=== SCRAPER STATUS REPORT ===\n")
        
        # Check all stores
        stores = db.query(Store).all()
        print(f"Total stores: {len(stores)}")
        
        # Check product counts by store
        result = db.query(Store.name, Store.id, func.count(Product.id).label('product_count')).outerjoin(
            Product, Store.id == Product.store_id
        ).group_by(Store.name, Store.id).order_by(Store.name).all()

        print("\nProducts by Store:")
        total_products = 0
        stores_with_products = 0
        
        for store_name, store_id, count in result:
            if count > 0:
                stores_with_products += 1
            print(f"  {store_name} (ID: {store_id}): {count} products")
            total_products += count

        print(f"\nSummary:")
        print(f"  - Total stores: {len(stores)}")
        print(f"  - Stores with products: {stores_with_products}")
        print(f"  - Total products: {total_products}")

        # Check products with images
        products_with_images = db.query(Product).filter(Product.image_data.isnot(None)).count()
        print(f"  - Products with images: {products_with_images}")
        
        # Show latest 5 products added
        latest_products = db.query(Product).order_by(Product.id.desc()).limit(5).all()
        print(f"\nLatest 5 products added:")
        for product in latest_products:
            store = db.query(Store).filter(Store.id == product.store_id).first()
            store_name = store.name if store else "Unknown"
            image_status = "✓ Image" if product.image_data else "✗ No image"
            print(f"  - {product.name} ({store_name}) - €{product.price} - {image_status}")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()
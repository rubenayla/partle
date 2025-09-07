#!/usr/bin/env python3
"""
Test script to verify scraped products get the 'in-store' tag
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.db.session import SessionLocal
from app.db.models import Product, Store, Tag

def test_add_product_with_tag():
    db = SessionLocal()
    
    try:
        # Get the BRICO DEPOT store
        store = db.query(Store).filter(Store.id == 4064).first()
        if not store:
            print("Error: BRICO DEPOT store not found")
            return
            
        # Get the in-store tag
        in_store_tag = db.query(Tag).filter(Tag.name == "in-store").first()
        if not in_store_tag:
            print("Error: 'in-store' tag not found")
            return
            
        # Create a test product
        test_product = Product(
            name="Test Hammer (Scraped Product)",
            price=19.99,
            description="Heavy duty hammer for construction work",
            store_id=store.id,
            creator_id=1,  # System user
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add the in-store tag
        test_product.tags.append(in_store_tag)
        
        # Save to database
        db.add(test_product)
        db.commit()
        db.refresh(test_product)
        
        print(f"✓ Created product: {test_product.name}")
        print(f"  Store: {store.name}")
        print(f"  Tags: {', '.join([t.name for t in test_product.tags])}")
        print(f"  ID: {test_product.id}")
        
        # Verify it was saved correctly
        saved_product = db.query(Product).filter(Product.id == test_product.id).first()
        if saved_product:
            tags = ', '.join([t.name for t in saved_product.tags])
            print(f"\n✓ Verification: Product saved with tags: [{tags}]")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_add_product_with_tag()
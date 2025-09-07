#!/usr/bin/env python3
"""
Update all products from physical stores to have the 'in-store' tag
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.models import Product, Store, Tag
from sqlalchemy import and_

def update_product_tags():
    db = SessionLocal()
    
    try:
        # Get the in-store tag
        in_store_tag = db.query(Tag).filter(Tag.name == "in-store").first()
        if not in_store_tag:
            print("Error: 'in-store' tag not found")
            return
            
        # Get all physical stores (stores that represent actual physical locations)
        # These are typically hardware stores, not online stores
        physical_store_keywords = [
            'brico', 'leroy', 'ferret', 'bauhaus', 'depot', 
            'hardware', 'tools', 'construction', 'bricolaje'
        ]
        
        # Get all products that should have in-store tag
        products_to_update = []
        
        for keyword in physical_store_keywords:
            stores = db.query(Store).filter(Store.name.ilike(f'%{keyword}%')).all()
            for store in stores:
                # Get products from this store that don't have the in-store tag
                products = db.query(Product).filter(
                    Product.store_id == store.id
                ).all()
                
                for product in products:
                    if in_store_tag not in product.tags:
                        products_to_update.append(product)
        
        print(f"Found {len(products_to_update)} products to update with 'in-store' tag")
        
        # Update products in batches
        updated_count = 0
        skipped_count = 0
        
        for product in products_to_update:
            try:
                # Check if product already has the tag
                if in_store_tag not in product.tags:
                    product.tags.append(in_store_tag)
                    db.flush()  # Flush to catch duplicate errors early
                    updated_count += 1
                else:
                    skipped_count += 1
                
                # Commit every 100 products
                if (updated_count + skipped_count) % 100 == 0:
                    db.commit()
                    print(f"  Processed {updated_count + skipped_count} products (updated: {updated_count}, skipped: {skipped_count})...")
                    
            except Exception as e:
                # Skip products that already have the tag
                db.rollback()
                skipped_count += 1
                continue
        
        # Final commit
        db.commit()
        
        print(f"\n✓ Successfully updated {updated_count} products with 'in-store' tag")
        if skipped_count > 0:
            print(f"  Skipped {skipped_count} products (already had tag or duplicates)")
        
        # Verify the update
        sample_products = db.query(Product).join(Product.tags).filter(
            Tag.name == "in-store"
        ).limit(5).all()
        
        print("\nSample of updated products:")
        for p in sample_products:
            print(f"  - {p.name[:50]}... (Store ID: {p.store_id})")
        
        total_with_tag = db.query(Product).join(Product.tags).filter(
            Tag.name == "in-store"
        ).count()
        
        print(f"\nTotal products with 'in-store' tag: {total_with_tag}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_product_tags()
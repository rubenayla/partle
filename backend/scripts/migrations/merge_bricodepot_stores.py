#!/usr/bin/env python3
"""
Script to merge duplicate Bricodepot/Brico Depot stores into a single canonical store.

Analysis shows:
- 5 main Bricodepot/Brico Depot stores (IDs: 1026, 1048, 3114, 3165, 4064)
- 40 numbered "Brico Dépôt_X" duplicates
- All stores have 0 products, so no reassignment needed

Canonical store will be: "Bricodepot" (chain type) with homepage
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.db.models import Store, Product, StoreType

def merge_bricodepot_stores():
    db = SessionLocal()
    try:
        # Get all Bricodepot/Brico Depot variations
        bricodepot_stores = db.query(Store).filter(
            Store.name.ilike('%bricodepot%') |
            Store.name.ilike('%brico%depot%') |
            Store.name.like('Brico Dépôt_%')
        ).all()
        
        print(f"Found {len(bricodepot_stores)} Bricodepot/Brico Depot stores to merge")
        
        # Create or update canonical store
        canonical_store = db.query(Store).filter(Store.name == "Bricodepot").first()
        if not canonical_store:
            # Create new canonical store
            canonical_store = Store(
                name="Bricodepot",
                type=StoreType.chain,
                homepage="https://www.bricodepot.es/"
            )
            db.add(canonical_store)
            db.flush()  # Get the ID
            print(f"Created canonical store 'Bricodepot' with ID: {canonical_store.id}")
        else:
            # Update existing canonical store
            canonical_store.type = StoreType.chain
            canonical_store.homepage = "https://www.bricodepot.es/"
            print(f"Updated canonical store 'Bricodepot' (ID: {canonical_store.id})")
        
        stores_to_delete = []
        products_reassigned = 0
        
        for store in bricodepot_stores:
            if store.id == canonical_store.id:
                continue  # Skip the canonical store itself
            
            print(f"Processing store: {store.name} (ID: {store.id})")
            
            # Reassign products (though analysis shows all have 0 products)
            products = db.query(Product).filter(Product.store_id == store.id).all()
            for product in products:
                product.store_id = canonical_store.id
                products_reassigned += 1
            
            stores_to_delete.append(store)
        
        print(f"Reassigned {products_reassigned} products to canonical store")
        
        # Delete duplicate stores
        for store in stores_to_delete:
            print(f"Deleting duplicate store: {store.name} (ID: {store.id})")
            db.delete(store)
        
        # Commit all changes
        db.commit()
        
        print(f"Successfully merged {len(stores_to_delete)} stores into canonical 'Bricodepot' store")
        print(f"Canonical store ID: {canonical_store.id}")
        
    except Exception as e:
        db.rollback()
        print(f"Error during merge: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    merge_bricodepot_stores()
#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

sys.path.append(str(Path(__file__).parent.parent.parent))

from app.db.models import Store, Product, Tag

# Try loading from backend/.env first, then root .env
backend_env = Path(__file__).parent / '.env'
root_env = Path(__file__).parent.parent / '.env'

if backend_env.exists():
    load_dotenv(backend_env)
elif root_env.exists():
    load_dotenv(root_env)

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in .env")
    sys.exit(1)

# URL encode the password to handle special characters
if '@' in DATABASE_URL:
    # Parse the URL to properly encode the password
    parts = DATABASE_URL.split('@')
    if len(parts) == 2:
        creds_and_scheme = parts[0]
        host_and_db = parts[1]
        
        # Split out the password
        if '://' in creds_and_scheme and ':' in creds_and_scheme.split('://')[-1]:
            scheme_user = creds_and_scheme.rsplit(':', 1)[0]
            password = creds_and_scheme.rsplit(':', 1)[1]
            
            # URL encode the password
            encoded_password = quote_plus(password)
            DATABASE_URL = f"{scheme_user}:{encoded_password}@{host_and_db}"

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def tag_stores_and_products():
    db = SessionLocal()
    try:
        # Create or get tags
        online_tag = db.query(Tag).filter_by(name="online").first()
        if not online_tag:
            online_tag = Tag(name="online")
            db.add(online_tag)
            print("Created 'online' tag")
        
        instore_tag = db.query(Tag).filter_by(name="in-store").first()
        if not instore_tag:
            instore_tag = Tag(name="in-store")
            db.add(instore_tag)
            print("Created 'in-store' tag")
        
        db.commit()
        
        # Get all stores
        stores = db.query(Store).all()
        
        online_stores = []
        instore_stores = []
        unclear_stores = []
        
        for store in stores:
            # Clear existing tags that we're about to reassign
            if online_tag in store.tags:
                store.tags.remove(online_tag)
            if instore_tag in store.tags:
                store.tags.remove(instore_tag)
            
            # Determine if store is online or has physical location
            has_physical_location = bool(store.address or store.lat or store.lon)
            
            # Common online-only store patterns
            online_keywords = ['amazon', 'ebay', 'aliexpress', 'online', 'web']
            is_likely_online = any(keyword in store.name.lower() for keyword in online_keywords)
            
            # Common physical store patterns
            physical_keywords = ['bauhaus', 'ikea', 'lidl', 'aldi', 'rewe', 'edeka', 'dm', 'rossmann']
            is_likely_physical = any(keyword in store.name.lower() for keyword in physical_keywords)
            
            if not has_physical_location and (is_likely_online or not is_likely_physical):
                # No physical location info and either likely online or not clearly physical
                store.tags.append(online_tag)
                online_stores.append(store)
            elif has_physical_location or is_likely_physical:
                # Has physical location info or is known physical store
                store.tags.append(instore_tag)
                instore_stores.append(store)
            else:
                # Unclear - no tags
                unclear_stores.append(store)
        
        db.commit()
        
        # Tag products based on their store's tags
        for store in online_stores:
            for product in store.products:
                if online_tag not in product.tags:
                    product.tags.append(online_tag)
                if instore_tag in product.tags:
                    product.tags.remove(instore_tag)
        
        for store in instore_stores:
            for product in store.products:
                if instore_tag not in product.tags:
                    product.tags.append(instore_tag)
                if online_tag in product.tags:
                    product.tags.remove(online_tag)
        
        # Products in unclear stores get no tags
        for store in unclear_stores:
            for product in store.products:
                if online_tag in product.tags:
                    product.tags.remove(online_tag)
                if instore_tag in product.tags:
                    product.tags.remove(instore_tag)
        
        db.commit()
        
        # Report results
        print(f"\n=== Tagging Results ===")
        print(f"Online stores: {len(online_stores)}")
        for store in online_stores[:10]:  # Show first 10
            print(f"  - {store.name}")
        if len(online_stores) > 10:
            print(f"  ... and {len(online_stores) - 10} more")
        
        print(f"\nIn-store (physical) stores: {len(instore_stores)}")
        for store in instore_stores[:10]:  # Show first 10
            print(f"  - {store.name} {f'({store.address})' if store.address else ''}")
        if len(instore_stores) > 10:
            print(f"  ... and {len(instore_stores) - 10} more")
        
        print(f"\nUnclear stores (no tags): {len(unclear_stores)}")
        for store in unclear_stores[:10]:  # Show first 10
            print(f"  - {store.name}")
        if len(unclear_stores) > 10:
            print(f"  ... and {len(unclear_stores) - 10} more")
        
        # Count products
        online_products = db.query(Product).join(Product.tags).filter(Tag.name == "online").count()
        instore_products = db.query(Product).join(Product.tags).filter(Tag.name == "in-store").count()
        
        print(f"\n=== Product Counts ===")
        print(f"Products tagged as online: {online_products}")
        print(f"Products tagged as in-store: {instore_products}")
        
    finally:
        db.close()


if __name__ == "__main__":
    tag_stores_and_products()
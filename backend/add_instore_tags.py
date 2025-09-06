#!/usr/bin/env python3
"""
Quick script to add in-store tags to products from physical stores.
Uses the simplified scraper config that loads from root .env
"""

from sqlalchemy import create_engine, text
from app.scraper.store_scrapers.config import config

def add_instore_tags():
    print("Adding in-store tags to products from physical stores...")
    
    engine = create_engine(config.DATABASE_URL, echo=False)
    
    with engine.connect() as conn:
        # Get or create the 'in-store' tag
        result = conn.execute(text("SELECT id FROM tags WHERE name = 'in-store'"))
        tag_row = result.fetchone()
        
        if not tag_row:
            # Create the in-store tag
            result = conn.execute(text("INSERT INTO tags (name) VALUES ('in-store') RETURNING id"))
            tag_id = result.fetchone()[0]
            print("Created 'in-store' tag")
        else:
            tag_id = tag_row[0]
            print(f"Found 'in-store' tag with ID: {tag_id}")
        
        # Get products from physical stores (stores with addresses) that don't have in-store tag yet
        result = conn.execute(text("""
            SELECT DISTINCT p.id, s.name
            FROM products p
            JOIN stores s ON p.store_id = s.id
            LEFT JOIN product_tags pt ON p.id = pt.product_id AND pt.tag_id = :tag_id
            WHERE s.address IS NOT NULL 
              AND s.address != ''
              AND pt.product_id IS NULL
        """), {"tag_id": tag_id})
        
        products_to_tag = list(result)
        
        if not products_to_tag:
            print("No products need in-store tags")
            return
        
        print(f"Found {len(products_to_tag)} products from physical stores to tag")
        
        # Add in-store tags in batches
        batch_size = 1000
        total_tagged = 0
        
        for i in range(0, len(products_to_tag), batch_size):
            batch = products_to_tag[i:i + batch_size]
            
            # Insert product_tags for this batch
            values = [{"product_id": product_id, "tag_id": tag_id} for product_id, _ in batch]
            
            conn.execute(text("""
                INSERT INTO product_tags (product_id, tag_id)
                VALUES (:product_id, :tag_id)
                ON CONFLICT (product_id, tag_id) DO NOTHING
            """), values)
            
            total_tagged += len(batch)
            print(f"Tagged {total_tagged}/{len(products_to_tag)} products...")
        
        # Commit the transaction
        conn.commit()
        
        print(f"✅ Successfully added 'in-store' tags to {len(products_to_tag)} products!")

if __name__ == "__main__":
    add_instore_tags()
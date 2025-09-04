#!/usr/bin/env python3
"""Remove all products with example.com URLs from the database."""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use Hetzner production database directly
DATABASE_URL = "postgresql://partle_user:v4zxTX7VN2Ljynlhon1fLg==@91.98.68.236:5432/partle"

def main():
    """Main function to check and remove example.com products."""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # First, check how many products have example.com URLs
        check_query = """
        SELECT COUNT(*) as count, 
               STRING_AGG(DISTINCT store_id::text, ', ') as store_ids
        FROM products 
        WHERE url LIKE '%example.com%'
        """
        
        result = conn.execute(text(check_query))
        row = result.fetchone()
        count = row[0]
        store_ids = row[1] if row[1] else 'None'
        
        print(f"Found {count} products with example.com URLs")
        print(f"From store IDs: {store_ids}")
        
        if count > 0:
            # Show a sample of products to be deleted
            sample_query = """
            SELECT id, name, url, store_id, price
            FROM products 
            WHERE url LIKE '%example.com%'
            LIMIT 5
            """
            
            print("\nSample of products to be deleted:")
            sample_result = conn.execute(text(sample_query))
            for product in sample_result:
                print(f"  ID: {product.id}, Name: {product.name[:50]}, URL: {product.url}")
            
            # Delete all products with example.com URLs
            delete_query = """
            DELETE FROM products 
            WHERE url LIKE '%example.com%'
            RETURNING id
            """
            
            print(f"\nDeleting {count} products...")
            delete_result = conn.execute(text(delete_query))
            deleted_ids = [row[0] for row in delete_result]
            conn.commit()
            
            print(f"Successfully deleted {len(deleted_ids)} products with example.com URLs")
            
            # Verify deletion
            verify_query = """
            SELECT COUNT(*) as count
            FROM products 
            WHERE url LIKE '%example.com%'
            """
            
            verify_result = conn.execute(text(verify_query))
            remaining = verify_result.fetchone()[0]
            
            if remaining == 0:
                print("✓ Verification successful: No products with example.com URLs remain")
            else:
                print(f"⚠ Warning: {remaining} products with example.com URLs still exist")
        else:
            print("No products with example.com URLs found. Nothing to delete.")

if __name__ == "__main__":
    main()
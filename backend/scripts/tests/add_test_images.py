#!/usr/bin/env python3
"""
Quick test to add images to existing products in Hetzner database
"""

import requests
import mimetypes
import os
from urllib.parse import urlparse
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.models import Product
from dotenv import load_dotenv

# Load environment variables from root .env
root_env = Path(__file__).parent.parent / '.env'
load_dotenv(root_env)

def download_image(image_url):
    """Download an image and return binary data, filename, and content type."""
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        image_data = response.content
        content_type = response.headers.get('content-type', 'image/jpeg')
        
        # Extract filename from URL
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename or '.' not in filename:
            extension = mimetypes.guess_extension(content_type) or '.jpg'
            filename = f"test_image_{abs(hash(image_url)) % 10000}{extension}"
            
        return image_data, filename, content_type
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")
        return None, None, None

def main():
    # Connect to database from environment
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("Error: DATABASE_URL environment variable is required")
        return
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = SessionLocal()
    
    try:
        # Find products with image URLs but no image data
        products_with_urls = db.query(Product).filter(
            Product.image_url.isnot(None),
            Product.image_data.is_(None)
        ).limit(3).all()
        
        print(f"Found {len(products_with_urls)} products with image URLs to process")
        
        for product in products_with_urls:
            print(f"Processing: {product.name} - {product.image_url}")
            
            # Download image
            image_data, filename, content_type = download_image(product.image_url)
            
            if image_data:
                product.image_data = image_data
                product.image_filename = filename
                product.image_content_type = content_type
                
                print(f"  Added image: {filename} ({len(image_data)} bytes)")
            else:
                print(f"  Failed to download image")
        
        # Commit changes
        db.commit()
        
        # Check results
        with_images = db.query(Product).filter(Product.image_data.isnot(None)).count()
        print(f"\nSuccess! Now {with_images} products have image data in database")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()
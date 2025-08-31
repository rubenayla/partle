#!/usr/bin/env python3
"""
Quick test script to add some products with images from external URLs
to test the image download and display functionality.
"""

import requests
import mimetypes
import os
from urllib.parse import urlparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.models import Product, Store
from app.scraper.store_scrapers.config import config

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
            filename = f"image_{abs(hash(image_url)) % 10000}{extension}"
            
        return image_data, filename, content_type
    except Exception as e:
        print(f"Failed to download {image_url}: {e}")
        return None, None, None

def main():
    # Connect to database
    engine = create_engine(config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db = SessionLocal()
    
    # Get or create a test store
    store = db.query(Store).first()
    if not store:
        print("No stores found in database. Please add a store first.")
        return
        
    print(f"Using store: {store.name} (ID: {store.id})")
    
    # Test products with images
    test_products = [
        {
            'name': 'Test Hammer with Image',
            'description': 'A high-quality hammer for construction work',
            'price': 25.99,
            'image_url': 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=400&h=400&fit=crop'
        },
        {
            'name': 'Test Screwdriver Set',
            'description': 'Professional screwdriver set with multiple sizes',
            'price': 39.99,
            'image_url': 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=400&h=400&fit=crop'
        },
        {
            'name': 'Test Power Drill',
            'description': 'Cordless power drill with battery',
            'price': 89.99,
            'image_url': 'https://images.unsplash.com/photo-1615228936080-765ab71e1976?w=400&h=400&fit=crop'
        }
    ]
    
    for product_data in test_products:
        try:
            print(f"Processing: {product_data['name']}")
            
            # Check if product already exists
            existing = db.query(Product).filter(Product.name == product_data['name']).first()
            if existing:
                print(f"  Product already exists, skipping")
                continue
            
            # Download image
            image_data, filename, content_type = download_image(product_data['image_url'])
            
            if image_data:
                print(f"  Downloaded image: {filename} ({len(image_data)} bytes)")
                
                # Create product with image data
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    image_url=product_data['image_url'],
                    image_data=image_data,
                    image_filename=filename,
                    image_content_type=content_type,
                    store_id=store.id,
                    creator_id=config.DEFAULT_CREATOR_ID
                )
                
                db.add(product)
                print(f"  Added product with image data")
            else:
                print(f"  Failed to download image, creating product without image data")
                
                # Create product without image data
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    image_url=product_data['image_url'],
                    store_id=store.id,
                    creator_id=config.DEFAULT_CREATOR_ID
                )
                
                db.add(product)
                
        except Exception as e:
            print(f"  Error processing {product_data['name']}: {e}")
            continue
    
    # Commit all changes
    try:
        db.commit()
        print("All products committed successfully!")
        
        # Show summary
        total_products = db.query(Product).count()
        products_with_images = db.query(Product).filter(Product.image_data.isnot(None)).count()
        print(f"Total products: {total_products}")
        print(f"Products with image data: {products_with_images}")
        
    except Exception as e:
        print(f"Error committing changes: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()
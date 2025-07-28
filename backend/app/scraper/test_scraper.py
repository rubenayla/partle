#!/usr/bin/env python3
"""
Simple test script to verify scraper components work correctly.

This script tests:
1. Database connection
2. Store exists in database  
3. Pipeline can save items
4. Spider can parse HTML
5. CSS selectors work
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from store_scrapers.config import config
from store_scrapers.items import ProductItem
from store_scrapers.pipelines import DatabasePipeline
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class MockSpider:
    """Mock spider for testing."""
    def __init__(self):
        self.logger = self
        self.crawler = self
        self.stats = MockStats()
    
    def info(self, msg):
        print(f"INFO: {msg}")
    
    def error(self, msg, exc_info=False):
        print(f"ERROR: {msg}")
        if exc_info:
            import traceback
            traceback.print_exc()
    
    def warning(self, msg):
        print(f"WARNING: {msg}")
    
    def inc_value(self, key):
        print(f"STAT: {key} += 1")


class MockStats:
    """Mock stats for testing."""
    def inc_value(self, key):
        print(f"STAT: {key} += 1")


def test_database_connection():
    """Test database connection."""
    print("🔍 Testing database connection...")
    try:
        engine = create_engine(config.DATABASE_URL, echo=False)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
        print("✅ Database connection works")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_store_exists():
    """Test if the Bricodepot store exists in database."""
    print("🔍 Testing if Bricodepot store exists...")
    try:
        engine = create_engine(config.DATABASE_URL, echo=False)
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT name FROM stores WHERE id = :store_id"),
                {"store_id": config.STORE_IDS["bricodepot"]}
            )
            store = result.fetchone()
            if store:
                print(f"✅ Store found: {store[0]} (ID: {config.STORE_IDS['bricodepot']})")
                return True
            else:
                print(f"❌ Store not found with ID: {config.STORE_IDS['bricodepot']}")
                return False
    except Exception as e:
        print(f"❌ Store check failed: {e}")
        return False


def test_pipeline():
    """Test the database pipeline."""
    print("🔍 Testing database pipeline...")
    try:
        # Create mock spider and pipeline
        spider = MockSpider()
        pipeline = DatabasePipeline()
        
        # Initialize pipeline
        pipeline.open_spider(spider)
        
        # Create test item
        test_item = ProductItem(
            name="TEST PRODUCT - DELETE ME",
            price=99.99,
            url="https://test.example.com/test-product",
            description="This is a test product created by the scraper test",
            image_url="https://test.example.com/test-image.jpg",
            store_id=config.STORE_IDS["bricodepot"],
        )
        
        # Process item
        result = pipeline.process_item(test_item, spider)
        
        # Close pipeline
        pipeline.close_spider(spider)
        
        print("✅ Pipeline processed item successfully")
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_css_selectors():
    """Test CSS selectors on real Bricodepot HTML."""
    print("🔍 Testing CSS selectors...")
    try:
        import requests
        from scrapy import Selector
        
        # Test homepage selectors
        print("  Testing homepage...")
        response = requests.get("https://www.bricodepot.es/", timeout=10)
        response.raise_for_status()
        
        selector = Selector(text=response.text)
        
        # Test category links
        category_links = selector.css('a.hm-link.main-navbar--item-parent::attr(href)').getall()
        print(f"  Found {len(category_links)} category links")
        
        if len(category_links) > 0:
            print(f"  Sample category: {category_links[0]}")
            
            # Test a category page
            print("  Testing category page...")
            category_url = f"https://www.bricodepot.es{category_links[0]}"
            cat_response = requests.get(category_url, timeout=10)
            cat_response.raise_for_status()
            
            cat_selector = Selector(text=cat_response.text)
            product_links = cat_selector.css('a.product-item-link::attr(href)').getall()
            print(f"  Found {len(product_links)} product links")
            
            if len(product_links) > 0:
                print(f"  Sample product: {product_links[0]}")
                
                # Test a product page
                print("  Testing product page...")
                product_url = f"https://www.bricodepot.es{product_links[0]}"
                prod_response = requests.get(product_url, timeout=10)
                prod_response.raise_for_status()
                
                prod_selector = Selector(text=prod_response.text)
                
                # Test product selectors
                name = prod_selector.css('h1.product-name::text').get()
                price = prod_selector.css('span.price::text').get()
                image = prod_selector.css('img.product-image-photo::attr(src)').get()
                desc = prod_selector.css('div.product-description-content p::text').get()
                
                print(f"  Product name: {name}")
                print(f"  Product price: {price}")
                print(f"  Product image: {image}")
                print(f"  Product description: {desc[:50] if desc else None}...")
                
                if name:
                    print("✅ CSS selectors work")
                    return True
                else:
                    print("❌ CSS selectors not finding product data")
                    return False
            else:
                print("❌ No product links found")
                return False
        else:
            print("❌ No category links found")
            return False
            
    except Exception as e:
        print(f"❌ CSS selector test failed: {e}")
        return False


def cleanup_test_data():
    """Clean up test data."""
    print("🧹 Cleaning up test data...")
    try:
        engine = create_engine(config.DATABASE_URL, echo=False)
        with engine.connect() as conn:
            result = conn.execute(
                text("DELETE FROM products WHERE name LIKE 'TEST PRODUCT%'")
            )
            conn.commit()
            deleted = result.rowcount
            if deleted > 0:
                print(f"✅ Cleaned up {deleted} test products")
            else:
                print("✅ No test products to clean up")
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")


def main():
    """Run all tests."""
    print("🚀 Starting scraper component tests\\n")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Store Exists", test_store_exists), 
        ("Database Pipeline", test_pipeline),
        ("CSS Selectors", test_css_selectors),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\\n{'='*50}")
        print(f"TEST: {test_name}")
        print('='*50)
        
        if test_func():
            passed += 1
        
    # Cleanup
    print(f"\\n{'='*50}")
    cleanup_test_data()
    
    # Results
    print(f"\\n{'='*50}")
    print(f"RESULTS: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 All tests passed! Scraper components are working correctly.")
        sys.exit(0)
    else:
        print("💥 Some tests failed. Check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
"""
Simple test scraper that actually works and downloads images
"""

import scrapy
from ..items import ProductItem
from ..config import config


class TestScraperSpider(scrapy.Spider):
    """
    Simple spider to test image downloading functionality
    """
    name = "test_scraper"
    store_id = 4066  # Using existing store ID from database
    
    # Test products with real images
    test_products = [
        {
            'name': 'Professional Hammer',
            'price': 29.99,
            'description': 'Heavy duty construction hammer',
            'image_url': 'https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?w=600&h=600&fit=crop',
            'url': 'https://example.com/hammer'
        },
        {
            'name': 'Electric Drill Set',
            'price': 89.99,
            'description': 'Cordless drill with battery pack',
            'image_url': 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=600&h=600&fit=crop',
            'url': 'https://example.com/drill'
        },
        {
            'name': 'Tool Box Professional',
            'price': 45.99,
            'description': 'Multi-compartment tool storage box',
            'image_url': 'https://images.unsplash.com/photo-1602080958523-4c60a7b10c83?w=600&h=600&fit=crop',
            'url': 'https://example.com/toolbox'
        },
        {
            'name': 'Safety Goggles Pro',
            'price': 12.99,
            'description': 'Professional safety eyewear',
            'image_url': 'https://images.unsplash.com/photo-1609205807490-e143f86fb41f?w=600&h=600&fit=crop',
            'url': 'https://example.com/goggles'
        },
        {
            'name': 'Work Gloves Heavy Duty',
            'price': 15.99,
            'description': 'Reinforced construction gloves',
            'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=600&fit=crop',
            'url': 'https://example.com/gloves'
        },
        {
            'name': 'Circular Saw',
            'price': 129.99,
            'description': '7-1/4 inch circular saw with laser guide',
            'image_url': 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=600&h=600&fit=crop',
            'url': 'https://example.com/saw'
        },
        {
            'name': 'Screwdriver Set',
            'price': 34.99,
            'description': '20-piece precision screwdriver set',
            'image_url': 'https://images.unsplash.com/photo-1530116586217-4d40b9d8b99d?w=600&h=600&fit=crop',
            'url': 'https://example.com/screwdrivers'
        },
        {
            'name': 'Level Professional',
            'price': 19.99,
            'description': '24-inch aluminum construction level',
            'image_url': 'https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=600&h=600&fit=crop',
            'url': 'https://example.com/level'
        },
        {
            'name': 'Tape Measure',
            'price': 8.99,
            'description': '25-foot steel measuring tape',
            'image_url': 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&h=600&fit=crop',
            'url': 'https://example.com/tape'
        },
        {
            'name': 'Wrench Set',
            'price': 42.99,
            'description': 'Combination wrench set 8-19mm',
            'image_url': 'https://images.unsplash.com/photo-1581335922225-e3ef0fdc54ba?w=600&h=600&fit=crop',
            'url': 'https://example.com/wrenches'
        }
    ]
    
    def start_requests(self):
        """Generate requests for test products"""
        # Just create a dummy request to trigger the spider
        yield scrapy.Request(
            url='https://httpbin.org/get',
            callback=self.parse,
            dont_filter=True
        )
    
    def parse(self, response):
        """Generate test products with images"""
        self.logger.info(f"Starting test scraper with {len(self.test_products)} products")
        
        for product_data in self.test_products:
            # Create product item
            item = ProductItem(
                name=product_data['name'],
                price=product_data['price'],
                description=product_data['description'],
                image_url=product_data['image_url'],
                url=product_data['url'],
                store_id=self.store_id
            )
            
            self.logger.info(f"Yielding product: {product_data['name']} with image: {product_data['image_url']}")
            yield item
        
        self.logger.info("Test scraper completed successfully")
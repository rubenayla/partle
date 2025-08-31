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
    
    # Generate hundreds of test products with variations
    def generate_test_products(self):
        """Generate hundreds of test products programmatically."""
        import random
        
        base_products = [
            ('Hammer', 'Construction and demolition hammer'),
            ('Drill', 'Electric drill for various materials'),
            ('Saw', 'Cutting tool for wood and metal'),
            ('Wrench', 'Adjustable wrench for bolts and nuts'),
            ('Screwdriver', 'Precision screwdriver set'),
            ('Pliers', 'Grip and bend tool'),
            ('Level', 'Bubble level for accurate measurements'),
            ('Tape Measure', 'Measuring tape for distances'),
            ('Chisel', 'Wood and metal cutting chisel'),
            ('File', 'Metal smoothing file'),
            ('Sandpaper', 'Abrasive paper for smoothing'),
            ('Glue', 'Strong adhesive for repairs'),
            ('Nails', 'Construction fastening nails'),
            ('Screws', 'Threaded fasteners'),
            ('Bolts', 'Heavy duty fasteners'),
            ('Washers', 'Flat rings for fasteners'),
            ('Nuts', 'Threaded fastener companions'),
            ('Anchors', 'Wall mounting hardware'),
            ('Brackets', 'Support and mounting brackets'),
            ('Hinges', 'Door and cabinet hinges'),
        ]
        
        materials = ['Steel', 'Aluminum', 'Plastic', 'Wood', 'Composite', 'Carbon Fiber', 'Titanium', 'Brass']
        brands = ['ProTool', 'MasterCraft', 'PowerMax', 'PrecisionPro', 'DuraBuild', 'SpeedWork', 'UltraTech', 'MaxForce']
        sizes = ['Mini', 'Small', 'Medium', 'Large', 'XL', 'Professional', 'Industrial', 'Heavy Duty']
        
        products = []
        image_urls = [
            'https://images.unsplash.com/photo-1586864387967-d02ef85d93e8?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1602080958523-4c60a7b10c83?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1609205807490-e143f86fb41f?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1530116586217-4d40b9d8b99d?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=600&h=600&fit=crop',
            'https://images.unsplash.com/photo-1581335922225-e3ef0fdc54ba?w=600&h=600&fit=crop',
        ]
        
        for i, (product_base, description_base) in enumerate(base_products):
            # Generate 50 variations of each base product
            for j in range(50):
                material = random.choice(materials)
                brand = random.choice(brands)
                size = random.choice(sizes)
                
                name = f"{brand} {size} {material} {product_base}"
                price = round(random.uniform(5.99, 299.99), 2)
                description = f"{size} {material.lower()} {description_base.lower()} from {brand}"
                image_url = random.choice(image_urls)
                
                products.append({
                    'name': name,
                    'price': price,
                    'description': description,
                    'image_url': image_url,
                    'url': f'https://example.com/product-{i * 50 + j}'
                })
        
        return products
    
    @property
    def test_products(self):
        return self.generate_test_products()
    
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
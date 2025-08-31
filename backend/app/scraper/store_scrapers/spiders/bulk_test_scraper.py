"""
Bulk test scraper for generating thousands of products across multiple stores
"""

import scrapy
from ..items import ProductItem
from ..config import config


class BulkTestScraperSpider(scrapy.Spider):
    """
    Bulk test spider that generates thousands of products across multiple stores
    """
    name = "bulk_test_scraper"
    
    # Rotate between different store IDs
    store_ids = [5001, 5002, 5003, 5004, 5005, 5006]
    current_store_index = 0
    
    def get_next_store_id(self):
        """Get the next store ID in rotation."""
        store_id = self.store_ids[self.current_store_index]
        self.current_store_index = (self.current_store_index + 1) % len(self.store_ids)
        return store_id
    
    # Generate massive product catalog
    def generate_bulk_products(self):
        """Generate thousands of products programmatically."""
        import random
        
        # Expanded product categories
        categories = [
            ('Power Tools', [
                'Drill', 'Saw', 'Grinder', 'Sander', 'Router', 'Planer', 'Impact Driver',
                'Circular Saw', 'Jigsaw', 'Reciprocating Saw', 'Angle Grinder', 'Heat Gun'
            ]),
            ('Hand Tools', [
                'Hammer', 'Screwdriver', 'Wrench', 'Pliers', 'Chisel', 'File', 'Hacksaw',
                'Socket Set', 'Allen Keys', 'Utility Knife', 'Wire Cutters', 'Torx Set'
            ]),
            ('Fasteners', [
                'Screws', 'Bolts', 'Nuts', 'Washers', 'Nails', 'Anchors', 'Rivets',
                'Threaded Rod', 'Wing Nuts', 'Cap Screws', 'Machine Screws', 'Wood Screws'
            ]),
            ('Hardware', [
                'Brackets', 'Hinges', 'Handles', 'Knobs', 'Latches', 'Locks', 'Chains',
                'Casters', 'Drawer Slides', 'Cabinet Hardware', 'Door Hardware', 'Window Hardware'
            ]),
            ('Safety Equipment', [
                'Hard Hats', 'Safety Glasses', 'Work Gloves', 'Ear Protection', 'Respirators',
                'Safety Vests', 'Steel Toe Boots', 'Fall Protection', 'First Aid Kits', 'Safety Signs'
            ]),
            ('Electrical', [
                'Wire', 'Conduit', 'Outlets', 'Switches', 'Breakers', 'Junction Boxes',
                'Cable Ties', 'Wire Nuts', 'Electrical Tape', 'Multimeters', 'Test Lights'
            ]),
            ('Plumbing', [
                'Pipes', 'Fittings', 'Valves', 'Faucets', 'Toilets', 'Sinks', 'Pumps',
                'Pipe Cutters', 'Plungers', 'Drain Cleaners', 'Pipe Wrenches', 'Soldering Tools'
            ]),
            ('Building Materials', [
                'Lumber', 'Drywall', 'Insulation', 'Roofing', 'Siding', 'Concrete', 'Rebar',
                'Plywood', 'OSB', 'Cement Board', 'House Wrap', 'Flashing'
            ]),
        ]
        
        materials = ['Steel', 'Aluminum', 'Stainless Steel', 'Plastic', 'Wood', 'Composite', 
                    'Carbon Fiber', 'Titanium', 'Brass', 'Bronze', 'Copper', 'Zinc',
                    'Cast Iron', 'Galvanized', 'Chrome', 'Nickel Plated']
                    
        brands = ['ProTool', 'MasterCraft', 'PowerMax', 'PrecisionPro', 'DuraBuild', 'SpeedWork',
                 'UltraTech', 'MaxForce', 'ToughGear', 'ReliaBuild', 'WorkPro', 'BuildMaster',
                 'ToolForce', 'CraftPro', 'MegaTool', 'SuperBuild', 'EliteCraft', 'PremiumTool']
                 
        sizes = ['Mini', 'Compact', 'Small', 'Medium', 'Large', 'XL', 'XXL', 'Professional', 
                'Industrial', 'Heavy Duty', 'Commercial', 'Standard', 'Premium', 'Deluxe']
                
        features = ['Wireless', 'Cordless', 'Rechargeable', 'LED', 'Digital', 'Magnetic',
                   'Adjustable', 'Ergonomic', 'Anti-Slip', 'Rust Resistant', 'Waterproof',
                   'Precision', 'High Torque', 'Variable Speed', 'Quick Release', 'Auto-Lock']
        
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
        
        # Generate products for each category
        for category_name, category_products in categories:
            for product_base in category_products:
                # Generate 25 variations of each product
                for i in range(25):
                    material = random.choice(materials)
                    brand = random.choice(brands)
                    size = random.choice(sizes)
                    feature = random.choice(features)
                    
                    # Create varied product names
                    if random.choice([True, False]):
                        name = f"{brand} {size} {feature} {product_base}"
                    else:
                        name = f"{brand} {material} {product_base} - {size}"
                    
                    price = round(random.uniform(3.99, 899.99), 2)
                    description = f"{feature} {size.lower()} {material.lower()} {product_base.lower()} from {brand}. Perfect for {category_name.lower()} applications."
                    image_url = random.choice(image_urls)
                    store_id = self.get_next_store_id()
                    
                    products.append({
                        'name': name,
                        'price': price,
                        'description': description,
                        'image_url': image_url,
                        'url': f'https://example.com/product-{len(products)}',
                        'store_id': store_id
                    })
        
        return products
    
    @property
    def bulk_products(self):
        return self.generate_bulk_products()
    
    def start_requests(self):
        """Generate requests for bulk test products"""
        yield scrapy.Request(
            url='https://httpbin.org/get',
            callback=self.parse,
            dont_filter=True
        )
    
    def parse(self, response):
        """Generate thousands of test products"""
        products = self.bulk_products
        self.logger.info(f"Starting bulk test scraper with {len(products)} products across {len(self.store_ids)} stores")
        
        for i, product_data in enumerate(products):
            # Create product item
            item = ProductItem(
                name=product_data['name'],
                price=product_data['price'],
                description=product_data['description'],
                image_url=product_data['image_url'],
                url=product_data['url'],
                store_id=product_data['store_id']
            )
            
            if i % 100 == 0:  # Log progress every 100 products
                self.logger.info(f"Yielding product batch {i//100 + 1}: {product_data['name']}")
            
            yield item
        
        self.logger.info(f"Bulk test scraper completed successfully with {len(products)} products")
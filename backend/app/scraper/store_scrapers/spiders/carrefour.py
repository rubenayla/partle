"""
Carrefour Spain scraper
"""

import scrapy
import json
import re
from urllib.parse import urljoin

class CarrefourSpider(scrapy.Spider):
    name = 'carrefour'
    allowed_domains = ['carrefour.es']
    
    # Start with tools/hardware categories
    start_urls = [
        'https://www.carrefour.es/bricolaje-y-ferreteria/herramientas/cat20002/',
        'https://www.carrefour.es/bricolaje-y-ferreteria/electricidad/cat5640007/',
        'https://www.carrefour.es/jardin-y-exterior/herramientas-de-jardin/cat5660004/',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # 2 seconds between requests
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'ROBOTSTXT_OBEY': False,  # Many sites block scrapers via robots.txt
        'COOKIES_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'app.scraper.store_scrapers.middleware.RotateUserAgentMiddleware': 400,
            'app.scraper.store_scrapers.middleware.HeadersMiddleware': 401,
            'app.scraper.store_scrapers.middleware.CookieMiddleware': 402,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        }
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store ID for Carrefour (to be created in database)
        self.store_id = kwargs.get('store_id', 5010)  # Default store ID
    
    def parse(self, response):
        """Parse category page"""
        
        # Check if blocked
        if response.status == 403 or 'blocked' in response.text.lower():
            self.logger.error(f"Blocked at {response.url}")
            return
        
        # Look for product data in JSON-LD format
        scripts = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        
        for script in scripts:
            try:
                data = json.loads(script)
                
                # Check if it's a product list
                if isinstance(data, dict) and data.get('@type') == 'ItemList':
                    items = data.get('itemListElement', [])
                    for item in items:
                        if item.get('@type') == 'Product':
                            yield self.parse_product_data(item)
                
                # Check for individual products
                elif isinstance(data, dict) and data.get('@type') == 'Product':
                    yield self.parse_product_data(data)
                    
            except json.JSONDecodeError:
                continue
        
        # Also try to extract products from HTML
        products = response.css('.product-card')
        
        for product in products:
            # Extract product URL
            product_url = product.css('a::attr(href)').get()
            if product_url:
                # Follow product link for more details
                yield response.follow(product_url, self.parse_product)
        
        # Follow pagination
        next_page = response.css('.pagination-next::attr(href)').get()
        if not next_page:
            next_page = response.css('a[rel="next"]::attr(href)').get()
        
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_product(self, response):
        """Parse individual product page"""
        
        # Try to get JSON-LD data first
        scripts = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        
        for script in scripts:
            try:
                data = json.loads(script)
                if isinstance(data, dict) and data.get('@type') == 'Product':
                    return self.parse_product_data(data, response.url)
            except json.JSONDecodeError:
                continue
        
        # Fallback to HTML extraction
        name = response.css('h1.product-name::text').get()
        if not name:
            name = response.css('.product-header__name::text').get()
        
        price_text = response.css('.product-price__unit-price::text').get()
        if not price_text:
            price_text = response.css('.buybox__price::text').get()
        
        price = self.extract_price(price_text)
        
        description = response.css('.product-description::text').get()
        if not description:
            description = ' '.join(response.css('.characteristics-list li::text').getall())
        
        image_url = response.css('.product-image img::attr(src)').get()
        if not image_url:
            image_url = response.css('img.product-media__image::attr(src)').get()
        
        if name:
            yield {
                'name': name.strip(),
                'price': price,
                'description': description.strip() if description else '',
                'url': response.url,
                'image_url': urljoin(response.url, image_url) if image_url else None,
                'store_id': self.store_id,
                'in_stock': True,  # Assume in stock if on website
                'category': 'Tools & Hardware'
            }
    
    def parse_product_data(self, data, url=None):
        """Parse product from JSON-LD data"""
        
        name = data.get('name', '')
        
        # Get price from offers
        price = None
        offers = data.get('offers', {})
        if isinstance(offers, dict):
            price = offers.get('price')
        elif isinstance(offers, list) and offers:
            price = offers[0].get('price')
        
        description = data.get('description', '')
        image = data.get('image')
        
        if isinstance(image, list) and image:
            image_url = image[0]
        elif isinstance(image, str):
            image_url = image
        else:
            image_url = None
        
        return {
            'name': name,
            'price': float(price) if price else None,
            'description': description,
            'url': url or data.get('url'),
            'image_url': image_url,
            'store_id': self.store_id,
            'in_stock': offers.get('availability') == 'https://schema.org/InStock' if isinstance(offers, dict) else True,
            'category': 'Tools & Hardware'
        }
    
    def extract_price(self, price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None
        
        # Remove currency symbols and extract number
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', '.'))
        if price_match:
            try:
                return float(price_match.group())
            except ValueError:
                return None
        return None
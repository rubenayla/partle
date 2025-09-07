"""
Simple Rationalstock spider - direct product page scraping
"""

import scrapy
from ..items import ProductItem
from ..config import config


class RationalstockSimpleSpider(scrapy.Spider):
    """
    Simplified spider for Rationalstock - goes directly to product listings
    """
    name = "rationalstock_simple"
    allowed_domains = ["rationalstock.es"]
    store_id = config.STORE_IDS.get("rationalstock", 4066)
    
    # Direct links to actual tool categories from Rationalstock
    start_urls = [
        # Abrasive tools
        "https://www.rationalstock.es/catalogo/grupos/herramientas/herramientas-abrasivas/1005",
        # Cutting tools
        "https://www.rationalstock.es/catalogo/grupos/herramientas/herramientas-de-corte/1010",
        # Screwdrivers
        "https://www.rationalstock.es/catalogo/grupos/herramientas/destornilladores/1035",
        # Main tools category
        "https://www.rationalstock.es/catalogo/familias/herramientas/10",
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Be respectful
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': False,
    }

    def parse(self, response):
        """Parse category page and extract products"""
        
        # Extract product links
        product_links = response.css('a[href*="/producto/"]::attr(href)').getall()
        
        self.logger.info(f"Found {len(product_links)} products on {response.url}")
        
        # Follow each product link
        for link in product_links[:3]:  # Limit to first 3 per category for testing
            yield response.follow(link, self.parse_product)
        
        # Follow pagination if exists
        next_page = response.css('a.next::attr(href)').get()
        if not next_page:
            # Alternative pagination selectors
            next_page = response.css('a[rel="next"]::attr(href)').get()
        
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        """Parse individual product page"""
        
        # Extract product name
        name = response.css('h1.product-title::text').get()
        if not name:
            name = response.css('h1::text').get()
        if not name:
            name = response.css('.product-name::text').get()
        
        # Extract price
        price = None
        price_text = response.css('.product-price::text').get()
        if not price_text:
            price_text = response.css('.price::text').get()
        if not price_text:
            # Try to find price in any element containing €
            price_text = response.xpath('//*[contains(text(), "€")]/text()').get()
        
        if price_text:
            # Clean price text and extract number
            import re
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', '.'))
            if price_match:
                try:
                    price = float(price_match.group())
                except ValueError:
                    pass
        
        # Extract description
        description = response.css('.product-description::text').get()
        if not description:
            description = response.css('.description::text').get()
        if not description:
            # Get all text from product details
            description_parts = response.css('.product-details ::text').getall()
            if description_parts:
                description = ' '.join(description_parts).strip()
        
        # Extract image URL from meta tags (Rationalstock stores product images in meta tags)
        image_url = response.css('meta[itemprop="image"]::attr(content)').get()
        if not image_url:
            image_url = response.css('meta[property="og:image"]::attr(content)').get()
        if not image_url:
            image_url = response.css('meta[name="twitter:image"]::attr(content)').get()
        if not image_url:
            # Fallback to regular img tags
            image_url = response.css('.product-image img::attr(src)').get()
        if not image_url:
            image_url = response.css('img[alt*="producto"]::attr(src)').get()
        
        # Make absolute URL
        if image_url and not image_url.startswith('http'):
            image_url = response.urljoin(image_url)
        
        # Extract SKU/reference
        sku = response.css('.product-ref::text').get()
        if not sku:
            sku = response.xpath('//*[contains(text(), "Ref")]/following-sibling::text()').get()
        
        if name:
            yield ProductItem(
                name=name.strip(),
                price=price,
                url=response.url,
                description=description.strip() if description else f"SKU: {sku}" if sku else "",
                image_url=image_url,
                store_id=self.store_id,
            )
            
            self.logger.info(f"Scraped: {name[:50]}... | Price: {price} | Image: {bool(image_url)}")
        else:
            self.logger.warning(f"Could not extract product name from {response.url}")
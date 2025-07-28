"""
Simple version of Bricodepot spider without Playwright for testing.
"""

import scrapy
from ..items import ProductItem
from ..config import config


class BricodepotSimpleSpider(scrapy.Spider):
    """
    Simple spider for Brico Depot website without browser automation.
    """
    name = "bricodepot_simple"
    allowed_domains = ["bricodepot.es"]
    store_id = config.STORE_IDS["bricodepot"]
    
    # Start with a few specific product URLs for testing
    start_urls = [
        'https://www.bricodepot.es/',
    ]

    def parse(self, response):
        """Parse the homepage to extract category links."""
        self.logger.info(f"Parsing homepage: {response.url}")
        
        # Extract category links from the homepage navigation
        category_links = response.css('a.hm-link.main-navbar--item-parent::attr(href)').getall()
        self.logger.info(f"Found {len(category_links)} category links")
        
        for link in category_links[:2]:  # Limit to first 2 categories for testing
            full_url = response.urljoin(link)
            self.logger.info(f"Following category: {full_url}")
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_category,
                dont_filter=True,
            )

    def parse_category(self, response):
        """Parse a category page to extract product links."""
        self.logger.info(f"Parsing category: {response.url}")
        
        # Extract product links from the category page listings
        product_links = response.css('a.product-item-link::attr(href)').getall()
        self.logger.info(f"Found {len(product_links)} product links")
        
        for link in product_links[:3]:  # Limit to first 3 products for testing
            full_url = response.urljoin(link)
            self.logger.info(f"Following product: {full_url}")
            yield scrapy.Request(
                url=full_url,
                callback=self.parse_product,
                dont_filter=True,
            )

    def parse_product(self, response):
        """Parse a product page to extract product details."""
        self.logger.info(f"Parsing product: {response.url}")
        
        # Extract product name
        product_name = response.css('h1.product-name::text').get()
        if product_name:
            product_name = product_name.strip()

        # Extract price and clean it
        price = response.css('span.price::text').get()
        if price:
            price = price.strip().replace('.', '').replace(',', '.')

        # Extract description
        description = response.css('div.product-description-content p::text').get()
        if description:
            description = description.strip()

        # Extract image URL
        image_url = response.css('img.product-image-photo::attr(src)').get()

        # Log what we found
        self.logger.info(f"Extracted product: {product_name}")
        self.logger.info(f"Price: {price}")
        self.logger.info(f"Image URL: {image_url}")
        self.logger.info(f"Description: {description[:100] if description else None}...")

        if product_name:
            # Create and yield the product item
            product_item = ProductItem(
                name=product_name,
                price=float(price) if price else None,
                url=response.url,
                description=description,
                image_url=image_url,
                store_id=self.store_id,
            )

            yield product_item
        else:
            self.logger.warning(f"No product name found for {response.url}")
"""
Direct product URL scraper for multiple stores
"""

import scrapy
from ..items import ProductItem
from ..config import config


class ProductsDirectSpider(scrapy.Spider):
    """
    Spider that directly scrapes product URLs from various stores.
    """
    name = "products_direct"
    
    # Direct product URLs from various stores
    start_urls = [
        # Bricodepot products
        "https://www.bricodepot.es/martillo-de-carpintero-16-oz-8002000009",
        "https://www.bricodepot.es/taladro-percutor-18v-brushless-sin-bateria-makita-8435538601645",
        "https://www.bricodepot.es/sierra-circular-1200w-185mm-8435538636104",
        
        # Leroy Merlin products
        "https://www.leroymerlin.es/productos/herramientas/herramientas-manuales/martillos/martillo-de-carpintero-dexter-de-16-oz-15385516.html",
        "https://www.leroymerlin.es/productos/herramientas/herramientas-electricas/taladros/taladro-percutor-a-bateria-bosch-18v-82507291.html",
        
        # Bauhaus products
        "https://www.bauhaus.es/martillos/wisent-martillo-de-carpintero/p/23746802",
        "https://www.bauhaus.es/taladros-percutores/bosch-professional-taladro-percutor-gsb-18v-21/p/26585685",
    ]
    
    def parse(self, response):
        """
        Parse product pages based on the domain.
        """
        domain = response.url.split('/')[2]
        
        if 'bricodepot' in domain:
            yield from self.parse_bricodepot(response)
        elif 'leroymerlin' in domain:
            yield from self.parse_leroymerlin(response)
        elif 'bauhaus' in domain:
            yield from self.parse_bauhaus(response)
    
    def parse_bricodepot(self, response):
        """Parse Bricodepot product page."""
        self.logger.info(f"Parsing Bricodepot product: {response.url}")
        
        # Extract product data
        name = response.css('h1.page-title span::text').get() or \
               response.css('h1.product-name::text').get() or \
               response.css('h1::text').get()
        
        if name:
            name = name.strip()
        
        price = response.css('span.price::text').get() or \
                response.css('.price-wrapper .price::text').get()
        
        if price:
            import re
            price = re.sub(r'[^\d,.]', '', price.strip()).replace(',', '.')
            try:
                price = float(price)
            except:
                price = None
        
        description = response.css('div.product-description-content::text').get() or \
                     response.css('.product-info-description::text').get()
        
        if description:
            description = description.strip()
        
        image_url = response.css('img.product-image-photo::attr(src)').get() or \
                   response.css('.product-image-main img::attr(src)').get() or \
                   response.css('img[itemprop="image"]::attr(src)').get()
        
        if image_url and not image_url.startswith('http'):
            image_url = response.urljoin(image_url)
        
        if name:
            yield ProductItem(
                name=name,
                price=price,
                url=response.url,
                description=description,
                image_url=image_url,
                store_id=config.STORE_IDS.get("bricodepot", 4064),
            )
            self.logger.info(f"Scraped Bricodepot: {name} | Price: {price} | Image: {image_url}")
    
    def parse_leroymerlin(self, response):
        """Parse Leroy Merlin product page."""
        self.logger.info(f"Parsing Leroy Merlin product: {response.url}")
        
        name = response.css('h1.product-title::text').get() or \
               response.css('h1[itemprop="name"]::text').get() or \
               response.css('h1::text').get()
        
        if name:
            name = name.strip()
        
        price = response.css('span.price-now::text').get() or \
                response.css('.product-price-value::text').get()
        
        if price:
            import re
            price = re.sub(r'[^\d,.]', '', price.strip()).replace(',', '.')
            try:
                price = float(price)
            except:
                price = None
        
        description = response.css('.product-description::text').get() or \
                     response.css('[itemprop="description"]::text').get()
        
        if description:
            description = description.strip()
        
        image_url = response.css('img.product-image::attr(src)').get() or \
                   response.css('.product-media img::attr(src)').get()
        
        if image_url and not image_url.startswith('http'):
            image_url = response.urljoin(image_url)
        
        if name:
            yield ProductItem(
                name=name,
                price=price,
                url=response.url,
                description=description,
                image_url=image_url,
                store_id=config.STORE_IDS.get("leroymerlin", 4063),
            )
            self.logger.info(f"Scraped Leroy Merlin: {name} | Price: {price} | Image: {image_url}")
    
    def parse_bauhaus(self, response):
        """Parse Bauhaus product page."""
        self.logger.info(f"Parsing Bauhaus product: {response.url}")
        
        name = response.css('h1.product-name::text').get() or \
               response.css('h1[itemprop="name"]::text').get() or \
               response.css('h1::text').get()
        
        if name:
            name = name.strip()
        
        price = response.css('.product-price .price::text').get() or \
                response.css('[itemprop="price"]::attr(content)').get()
        
        if price:
            import re
            price = re.sub(r'[^\d,.]', '', str(price).strip()).replace(',', '.')
            try:
                price = float(price)
            except:
                price = None
        
        description = response.css('.product-description::text').get() or \
                     response.css('[itemprop="description"]::text').get()
        
        if description:
            description = description.strip()
        
        image_url = response.css('img.product-image::attr(src)').get() or \
                   response.css('.product-gallery img::attr(src)').get()
        
        if image_url and not image_url.startswith('http'):
            image_url = response.urljoin(image_url)
        
        if name:
            yield ProductItem(
                name=name,
                price=price,
                url=response.url,
                description=description,
                image_url=image_url,
                store_id=config.STORE_IDS.get("bauhaus", 4065),
            )
            self.logger.info(f"Scraped Bauhaus: {name} | Price: {price} | Image: {image_url}")
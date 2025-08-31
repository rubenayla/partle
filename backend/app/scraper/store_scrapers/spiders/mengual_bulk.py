"""
Bulk Mengual spider for high-volume scraping - scrapes all major categories
"""

import scrapy
import re
from ..items import ProductItem
from ..config import config


class MengualBulkSpider(scrapy.Spider):
    """
    Bulk spider for Mengual.com - scrapes all major categories for maximum products.
    """
    name = "mengual_bulk"
    allowed_domains = ["mengual.com"]
    store_id = config.STORE_IDS.get("mengual", 4070)

    def start_requests(self):
        """Start with main category pages to find more product URLs."""
        category_urls = [
            # Hardware categories
            "https://www.mengual.com/tiradores-y-pomos",
            "https://www.mengual.com/bisagras",
            "https://www.mengual.com/guias-de-cajones", 
            "https://www.mengual.com/herrajes-para-armarios",
            "https://www.mengual.com/cerraduras-y-seguridad",
            "https://www.mengual.com/manetas-y-rosetas",
            
            # Kitchen & bath
            "https://www.mengual.com/accesorios-de-cocina",
            "https://www.mengual.com/accesorios-de-bano",
            "https://www.mengual.com/equipamiento-de-cocina-y-bano",
            
            # Tools & lighting
            "https://www.mengual.com/herramientas-electricas",
            "https://www.mengual.com/herramientas-manuales",
            "https://www.mengual.com/iluminacion",
            "https://www.mengual.com/accesorios-para-iluminacion",
            
            # Construction & furniture
            "https://www.mengual.com/herrajes-para-construccion",
            "https://www.mengual.com/herrajes-para-muebles",
            "https://www.mengual.com/sistemas-de-apertura",
            
            # Additional categories
            "https://www.mengual.com/perfiles-y-tubos",
            "https://www.mengual.com/tornilleria",
            "https://www.mengual.com/adhesivos-y-selladores",
        ]
        
        for url in category_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_category,
                dont_filter=True
            )

    def parse_category(self, response):
        """Parse category page to extract product links."""
        self.logger.info(f"Parsing category: {response.url}")
        
        # Extract product links using multiple patterns
        product_links = set()
        
        # Look for product URLs in href attributes
        for link in response.css('a::attr(href)').getall():
            if link and ('producto' in link.lower() or 'product' in link.lower() or 
                        (link.startswith('/') and len(link) > 10 and '-' in link)):
                if link.startswith('/'):
                    link = f"https://www.mengual.com{link}"
                product_links.add(link)
        
        # Also look for links that might be product pages based on URL patterns
        for link in response.css('a::attr(href)').getall():
            if link and link.startswith('/') and len(link.split('-')) >= 3:
                full_url = f"https://www.mengual.com{link}"
                product_links.add(full_url)
        
        self.logger.info(f"Found {len(product_links)} potential product links in {response.url}")
        
        # Follow product links
        for link in list(product_links)[:50]:  # Limit to 50 products per category
            yield scrapy.Request(
                url=link,
                callback=self.parse_product,
                dont_filter=True
            )

    def parse_product(self, response):
        """Parse product page using regex extraction from meta tags."""
        self.logger.info(f"Parsing product: {response.url}")
        
        html_content = response.text

        # Extract product name from meta tag og:title
        name = None
        name_match = re.search(r'<meta property="og:title" content="([^"]*)"', html_content)
        if name_match:
            import html
            name = html.unescape(name_match.group(1))

        # Extract price from meta tag
        price = None
        price_match = re.search(r'<meta property="product:price:amount" content="([^"]*)"', html_content)
        if price_match:
            try:
                price = float(price_match.group(1))
            except ValueError:
                price = None

        # Extract description from meta tags
        description = None
        desc_match = re.search(r'<meta property="og:description" content="([^"]*)"', html_content)
        if desc_match:
            import html
            desc_text = html.unescape(desc_match.group(1))
            if desc_text.strip():
                description = desc_text.strip()
        
        # Try regular meta description if og:description is empty
        if not description:
            desc_match = re.search(r'<meta name="description" content="([^"]*)"', html_content)
            if desc_match:
                import html
                desc_text = html.unescape(desc_match.group(1))
                if desc_text.strip():
                    description = desc_text.strip()

        # Extract image URL from meta tag og:image
        image_url = None
        img_match = re.search(r'<meta property="og:image" content="([^"]*)"', html_content)
        if img_match:
            image_url = img_match.group(1)
            if '?' in image_url:
                image_url = image_url.split('?')[0]

        # Create and yield the product item if we have basic info
        if name:
            product_item = ProductItem(
                name=name,
                price=price,
                url=response.url,
                description=description,
                image_url=image_url,
                store_id=self.store_id,
            )

            self.logger.info(f"Scraped bulk product: {name} | Price: {price} | Image: {bool(image_url)}")
            yield product_item
        else:
            self.logger.debug(f"No product name found for {response.url}")
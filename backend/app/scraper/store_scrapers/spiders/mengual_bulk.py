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

        # Patterns that indicate non-product pages (legal, guides, info pages)
        excluded_patterns = [
            'terminos', 'legal', 'privacidad', 'cookies', 'envio', 'pago',
            'procedimiento', 'calendario', 'delegaciones', 'showrooms',
            'incidencias', 'compliance', 'catalogos', 'historia', 'empresa',
            'cobertura', 'expediciones', 'instalacion', 'fotovoltaica',
            'guias-', 'catalogo', 'contacto', 'nosotros', 'blog', 'noticias'
        ]

        # Look for product URLs in href attributes
        for link in response.css('a::attr(href)').getall():
            if not link:
                continue

            # Skip if link contains excluded patterns
            link_lower = link.lower()
            if any(pattern in link_lower for pattern in excluded_patterns):
                continue

            # Skip category/listing pages
            if any(cat in link_lower for cat in ['/categoria/', '/categorias/', '/collections/']):
                continue

            # Look for specific product URL patterns
            # Mengual products typically have URLs like: /tirador-kimera, /cazoleta-rectangular
            if link.startswith('/'):
                # Must have at least one dash and be a reasonable length
                if '-' in link and 10 < len(link) < 100:
                    # Should not be a category page (those usually end with category names)
                    if not any(cat in link for cat in self.start_urls):
                        full_url = f"https://www.mengual.com{link}"
                        product_links.add(full_url)
            elif link.startswith('https://www.mengual.com/'):
                # Full URL - apply same filters
                path = link.replace('https://www.mengual.com/', '')
                if '-' in path and 10 < len(path) < 100:
                    if not any(cat in link for cat in self.start_urls):
                        product_links.add(link)

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

        # Create and yield the product item only if we have a valid product
        # A valid product should have a name and ideally a price
        # Exclude pages that are clearly not products
        excluded_name_patterns = [
            'términos', 'legal', 'catálogo', 'procedimiento', 'calendario',
            'delegaciones', 'showroom', 'incidencias', 'compliance',
            'instalación', 'cobertura', 'expediciones', 'historia'
        ]

        if name:
            # Check if this looks like a non-product page
            name_lower = name.lower()
            if any(pattern in name_lower for pattern in excluded_name_patterns):
                self.logger.debug(f"Skipping non-product page: {name} at {response.url}")
                return

            # Only yield products that have prices or look like actual products
            # Products without prices might be valid (price on request) but should have proper product names
            if price or (len(name) < 100 and '-' in name):
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
                self.logger.debug(f"Skipping item without price: {name} at {response.url}")
        else:
            self.logger.debug(f"No product name found for {response.url}")
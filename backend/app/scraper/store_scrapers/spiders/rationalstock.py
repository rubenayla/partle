"""
Scrapy spider for scraping product data from Rationalstock.

This spider navigates through categories, extracts product links, and then
scrapes detailed information for each product. Rationalstock is a B2B industrial
supplier with 32,000+ products and uses Apache server (no Cloudflare protection).
"""

import scrapy
from ..items import ProductItem
from ..config import config


class RationalstockSpider(scrapy.Spider):
    """
    Spider for Rationalstock website.
    """
    name = "rationalstock"
    allowed_domains = ["rationalstock.es"]
    store_id = config.STORE_IDS["rationalstock"]

    def start_requests(self):
        """
        Initiates the scraping process by sending a request to the Rationalstock homepage.
        No Playwright needed since it's Apache server without heavy JS.
        """
        yield scrapy.Request(
            url="https://www.rationalstock.es/",
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response):
        """
        Parses the homepage to extract category links and follows them.

        Args:
            response (scrapy.http.Response): The response object from the homepage.
        """
        # Extract category links from navigation
        category_selectors = [
            'nav a[href*="/catalogo/"]::attr(href)',
            '.menu a[href*="/catalogo/"]::attr(href)', 
            'a[href*="/categoria/"]::attr(href)',
            '.navigation a[href*="/"]::attr(href)',
            '.main-menu a[href*="/"]::attr(href)',
        ]
        
        category_links = []
        for selector in category_selectors:
            links = response.css(selector).getall()
            if links:
                # Filter for category pages
                valid_links = [
                    link for link in links 
                    if link and any(category in link.lower() for category in [
                        'catalogo', 'categoria', 'herramientas', 'ferreteria', 'tools',
                        'materiales', 'equipos', 'suministros', 'industrial'
                    ]) and not any(skip in link.lower() for skip in [
                        '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                        '/cuenta', '/cart', '/checkout', '/login', '/registro'
                    ])
                ]
                if valid_links:
                    category_links.extend(valid_links)
                    self.logger.info(f"Found {len(valid_links)} category links with selector: {selector}")
                    break
        
        # Fallback: try direct catalog page
        if not category_links:
            self.logger.info("No category links found, trying direct catalog access")
            category_links = ["/catalogo/"]
            
        for link in category_links:  # Process all categories to reach 32k+ products
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_category,
                dont_filter=True,
            )

    def parse_category(self, response):
        """
        Parses a category page to extract product links and follows them.

        Args:
            response (scrapy.http.Response): The response object from a category page.
        """
        self.logger.info(f"Parsing category: {response.url}")

        # Extract product links
        product_selectors = [
            '.product-item a::attr(href)',
            'a[href*="/producto/"]::attr(href)',
            'a[href*="/product/"]::attr(href)',
            '.product-link::attr(href)',
            '.item-link::attr(href)',
            'a[title*="Ver producto"]::attr(href)',
        ]
        
        product_links = []
        for selector in product_selectors:
            links = response.css(selector).getall()
            if links:
                # Filter to actual product links
                filtered_links = [
                    link for link in links 
                    if link and not any(skip in link.lower() for skip in [
                        '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                        '/categoria', '/category', '/cart', '/checkout', '/account'
                    ])
                ]
                if filtered_links:
                    product_links.extend(filtered_links)  # Process all products per category
                    self.logger.info(f"Selector '{selector}' found {len(filtered_links)} valid product links (using all)")
                    break
        
        # Also check for pagination links to get more products
        next_page_selectors = [
            'a[rel="next"]::attr(href)',
            '.pagination a[href*="page="]::attr(href)',
            '.next-page::attr(href)',
        ]
        
        for selector in next_page_selectors:
            next_page = response.css(selector).get()
            if next_page:
                yield scrapy.Request(
                    url=response.urljoin(next_page),
                    callback=self.parse_category,
                    dont_filter=True,
                )
                break
        
        if not product_links:
            self.logger.info(f"No product links found on {response.url}")
            return
        
        self.logger.info(f"Total product links found: {len(product_links)}")
        for link in product_links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_product,
                dont_filter=True,
            )

    def parse_product(self, response):
        """
        Parses a product page to extract product details.

        Args:
            response (scrapy.http.Response): The response object from a product page.
        """
        self.logger.info(f"Parsing product: {response.url}")

        # Extract product name
        product_name_selectors = [
            'h1.product-title::text',
            'h1.product-name::text',
            '.product-header h1::text',
            'h1::text',
            '.page-title h1::text',
        ]
        
        product_name = None
        for selector in product_name_selectors:
            name = response.css(selector).get()
            if name and name.strip():
                product_name = name.strip()
                break

        # Extract price
        price_selectors = [
            '.price::text',
            '.product-price::text',
            '.precio::text',
            '[class*="price"]::text',
        ]
        
        price = None
        for selector in price_selectors:
            price_text = response.css(selector).get()
            if price_text and price_text.strip():
                # Clean price: remove spaces, currency symbols
                cleaned_price = price_text.strip().replace('\xa0', '').replace('€', '').replace('$', '').replace(',', '.')
                try:
                    price = cleaned_price
                    break
                except:
                    continue

        # Extract description
        description_selectors = [
            '.product-description::text',
            '.product-info p::text',
            '.descripcion::text',
            '.description p::text',
        ]
        
        description = None
        for selector in description_selectors:
            desc = response.css(selector).get()
            if desc and desc.strip():
                description = desc.strip()
                break

        # Extract image URL
        image_selectors = [
            'img[src*="cataleg350"]::attr(src)',
            'img[src*="cataleg150"]::attr(src)', 
            'img[src*="/img_rational/img/catalog/"]::attr(src)',
            'img[src*="/img_rational/"]::attr(src)',
            '.product-image img::attr(src)',
            '.producto-imagen img::attr(src)',
            '.main-image img::attr(src)',
            'img[class*="product"]::attr(src)',
        ]
        
        image_url = None
        for selector in image_selectors:
            img = response.css(selector).get()
            if img:
                image_url = response.urljoin(img)
                break

        # Convert price to float
        price_float = None
        if price:
            try:
                import re
                numeric_price = re.sub(r'[^\d.]', '', str(price))
                if numeric_price:
                    price_float = float(numeric_price)
            except (ValueError, TypeError):
                self.logger.warning(f"Could not convert price '{price}' to float")

        # Create and yield the product item
        if product_name:
            product_item = ProductItem(
                name=product_name,
                price=price_float,
                url=response.url,
                description=description,
                image_url=image_url,
                store_id=self.store_id,
            )

            self.logger.info(f"Scraped product: {product_name} | Price: {price_float}")
            yield product_item
        else:
            self.logger.warning(f"No product name found for {response.url}")
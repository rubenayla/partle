"""
Scrapy spider for scraping product data from Brico Depot.

This spider navigates through categories, extracts product links, and then
scrapes detailed information for each product, including name, price,
description, and image URL. It saves this data directly to the database
using Scrapy pipelines.
"""

import scrapy
from ..items import ProductItem
from ..config import config


class BricodepotSpider(scrapy.Spider):
    """
    Spider for Brico Depot website.
    """
    name = "bricodepot"
    allowed_domains = ["bricodepot.es"]
    store_id = config.STORE_IDS["bricodepot"]

    def start_requests(self):
        """
        Initiates the scraping process by sending a request to the Brico Depot homepage.
        Uses Playwright for rendering the page.
        """
        yield scrapy.Request(
            url="https://www.bricodepot.es/",
            callback=self.parse,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_goto_kwargs={
                    'wait_until': 'domcontentloaded',
                    'timeout': 60000,
                },
                playwright_page_methods=[
                    {'method': 'wait_for_selector', 'args': ['body']},
                    {'method': 'wait_for_timeout', 'args': [5000]},  # Wait for Algolia to load products
                ],
            ),
            dont_filter=True,  # Ensures the request is not filtered even if it's already visited
        )

    async def parse(self, response):
        """
        Parses the homepage to extract category links and follows them.

        Args:
            response (scrapy.http.Response): The response object from the homepage.
        """
        try:
            page = response.meta["playwright_page"]
            html_content = await page.content()
            await page.close()
            response = response.replace(body=html_content, encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error processing homepage: {e}")
            return

        # Extract category links from the homepage navigation
        # Updated selectors based on current website structure
        category_selectors = [
            'a.hm-link::attr(href)',  # Main navigation links
            '.hm-level a[href*="/"]::attr(href)',  # Menu level links
            '.navigation .level0 a::attr(href)',  # Navigation level links
            '.nav-sections a[href*="/"]::attr(href)',  # Section navigation
        ]
        
        category_links = []
        for selector in category_selectors:
            links = response.css(selector).getall()
            if links:
                # Filter for category/product pages
                valid_links = [
                    link for link in links 
                    if link and any(category in link.lower() for category in [
                        'bricolaje', 'construccion', 'jardin', 'ferreteria', 'herramientas',
                        'material', 'productos', 'categoria', 'category'
                    ]) and not any(skip in link.lower() for skip in [
                        '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                        '/cuenta', '/cart', '/checkout'
                    ])
                ]
                if valid_links:
                    category_links.extend(valid_links)
                    self.logger.info(f"Found {len(valid_links)} category links with selector: {selector}")
                    break
        
        # If no category links found, try to find product pages directly
        if not category_links:
            self.logger.info("No category links found, trying to find product pages directly")
            # Try specific category pages that are known to have products
            category_links = [
                "/decoracion-iluminacion",
                "/ferreteria", 
                "/herramientas",
                "/construccion",
                "/jardin",
                "/ceramica",
                "/electricidad-domotica",
                "/pintura-drogueria"
            ]
        for link in category_links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_category,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_goto_kwargs={
                        'wait_until': 'domcontentloaded',
                        'timeout': 60000,
                    },
                    playwright_page_methods=[
                        {'method': 'wait_for_selector', 'args': ['body']},
                        {'method': 'wait_for_timeout', 'args': [5000]},  # Wait for Algolia to load products
                    ],
                ),
                dont_filter=True,
            )

    async def parse_category(self, response):
        """
        Parses a category page to extract product links and follows them.

        Args:
            response (scrapy.http.Response): The response object from a category page.
        """
        try:
            page = response.meta["playwright_page"]
            html_content = await page.content()
            await page.close()
            response = response.replace(body=html_content, encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error processing category page {response.url}: {e}")
            return

        # Extract product links - Look for various product link patterns
        product_selectors = [
            '.product-item a::attr(href)',         # Main product item links (WORKING!)
            'a[href*="/productos/"]::attr(href)',  # Direct product links
            'a[href*="/product/"]::attr(href)',    # Alternative product links
            '.product-item-link::attr(href)',      # Product item links
            '.ais-Hits-item a::attr(href)',        # Algolia InstantSearch hits
            '.algolia-hit a::attr(href)',          # Algolia hit links
            '[class*="hit"] a::attr(href)',        # Generic hit containers
            '[data-objectid] a::attr(href)',       # Algolia object IDs
            'a[href*=".html"]::attr(href)',        # HTML page links (likely products)
        ]
        
        product_links = []
        for selector in product_selectors:
            links = response.css(selector).getall()
            if links:
                # Filter to actual product links (not category/static links)
                filtered_links = [
                    link for link in links 
                    if link and not any(skip in link.lower() for skip in [
                        '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                        '/categoria', '/category', '/promociones', '/ofertas', '/cart',
                        '/checkout', '/account', '/search', 'identifier_brand'
                    ]) and (
                        # Accept product URLs like /espejo-clic-68-x-80-cm-8431949256265
                        '-' in link and  # Contains hyphens (typical product URLs)
                        any(char.isdigit() for char in link)  # Contains digits (often product codes)
                    )
                ]
                if filtered_links:
                    product_links.extend(filtered_links[:10])  # Limit to first 10 for testing
                    self.logger.info(f"Selector '{selector}' found {len(filtered_links)} valid product links (using first 10)")
                    break
        
        # If no product links found, skip this page (don't treat category pages as products)
        if not product_links:
            self.logger.info(f"No product links found on {response.url}, skipping category page")
            return
        
        self.logger.info(f"Total product links found: {len(product_links)}")
        for link in product_links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_product,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_goto_kwargs={
                        'wait_until': 'domcontentloaded',
                        'timeout': 60000,
                    },
                    playwright_page_methods=[
                        {'method': 'wait_for_selector', 'args': ['body']},
                        {'method': 'wait_for_timeout', 'args': [5000]},  # Wait for Algolia to load products
                    ],
                ),
                dont_filter=True,
            )

    async def parse_product(self, response):
        """
        Parses a product page to extract product details and sends them to the backend.

        Args:
            response (scrapy.http.Response): The response object from a product page.
        """
        try:
            page = response.meta["playwright_page"]
            html_content = await page.content()
            await page.close()
            response = response.replace(body=html_content, encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Error processing product page {response.url}: {e}")
            return

        # Extract product name - try multiple selectors
        product_name_selectors = [
            'h1.product-name::text',
            'h1[data-testid="product-title"]::text',
            '.product-item-name::text',
            '.product-title::text',
            'h1::text',
            '.page-title span::text',
            '[data-ui-id="page-title-wrapper"] h1::text',
        ]
        
        product_name = None
        for selector in product_name_selectors:
            name = response.css(selector).get()
            if name and name.strip():
                product_name = name.strip()
                break

        # Extract price - try multiple selectors
        price_selectors = [
            'span.price::text',
            '.price::text',
            '.price-wrapper .price::text',
            '[data-price-type="finalPrice"] .price::text',
            '.regular-price .price::text',
            '.price-container .price::text',
        ]
        
        price = None
        for selector in price_selectors:
            price_text = response.css(selector).get()
            if price_text and price_text.strip():
                # Clean price: remove spaces, non-breaking spaces, currency symbols
                cleaned_price = price_text.strip().replace('\xa0', '').replace('€', '').replace('$', '').replace(',', '.')
                try:
                    price = cleaned_price
                    break
                except:
                    continue

        # Extract description - try multiple selectors
        description_selectors = [
            'div.product-description-content p::text',
            '.product-info-description p::text',
            '.product-attribute-description::text',
            '.product-overview::text',
            '.short-description::text',
        ]
        
        description = None
        for selector in description_selectors:
            desc = response.css(selector).get()
            if desc and desc.strip():
                description = desc.strip()
                break

        # Extract image URL - try multiple selectors
        image_selectors = [
            'img.product-image-photo::attr(src)',
            '.product-image-main img::attr(src)',
            '.fotorama__img::attr(src)',
            '.product-media img::attr(src)',
        ]
        
        image_url = None
        for selector in image_selectors:
            img = response.css(selector).get()
            if img:
                image_url = response.urljoin(img)
                break

        # Convert price to float if possible
        price_float = None
        if price:
            try:
                # Remove any remaining non-numeric characters except dots
                import re
                numeric_price = re.sub(r'[^\d.]', '', str(price))
                if numeric_price:
                    price_float = float(numeric_price)
            except (ValueError, TypeError):
                self.logger.warning(f"Could not convert price '{price}' to float")

        # Create and yield the product item
        product_item = ProductItem(
            name=product_name,
            price=price_float,
            url=response.url,
            description=description,
            image_url=image_url,
            store_id=self.store_id,
        )

        self.logger.info(f"Scraped product: {product_name} | Price: {price_float} | URL: {response.url}")
        yield product_item
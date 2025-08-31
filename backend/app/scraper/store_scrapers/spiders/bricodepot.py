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
        
        # If no category links found, or limit to main productive categories
        if not category_links or len(category_links) > 50:
            self.logger.info("Using focused list of main product categories")
            # Focus on main categories that are most likely to have products
            category_links = [
                "/decoracion-iluminacion",
                "/herramientas", 
                "/herramientas/herramientas-manuales",
                "/herramientas/herramientas-electricas",
                "/herramientas/ofertas-herramientas",
                "/construccion",
                "/construccion/bloques-ladrillos",
                "/construccion/cemento-morteros",
                "/construccion/aislamiento",
                "/jardin",
                "/jardin/casetas-cobertizos",
                "/jardin/muebles-jardin", 
                "/jardin/barbacoas-hornos",
                "/ceramica",
                "/ceramica/pavimentos",
                "/ceramica/revestimientos",
                "/electricidad-domotica",
                "/electricidad-domotica/iluminacion",
                "/electricidad-domotica/material-electrico",
                "/pintura-drogueria",
                "/pintura-drogueria/pinturas",
                "/pintura-drogueria/herramientas-pintura",
                "/suelos-revestimientos-pared",
                "/suelos-revestimientos-pared/suelo-laminado",
                "/ferreteria/tornilleria",
                "/ferreteria/adhesivos-selladores"
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
            )

    async def parse_category(self, response):
        """
        Parses a category page to extract product links and follows them.
        Now handles pagination and JavaScript-loaded content.

        Args:
            response (scrapy.http.Response): The response object from a category page.
        """
        product_links = []
        pagination_links = []
        
        try:
            page = response.meta["playwright_page"]
            
            # Wait for JavaScript to load products (optimized timing)
            await page.wait_for_timeout(4000)
            
            # Try scrolling to trigger any lazy loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            
            # Look for "Load More" or "Ver más" buttons and click them multiple times
            load_more_selectors = [
                'button:has-text("Cargar más")',
                'button:has-text("Ver más")',
                'button:has-text("Mostrar más")',
                '.load-more',
                '.show-more',
                '[data-testid="load-more"]',
                'button[class*="load"]',
                'a:has-text("Ver todos")',
            ]
            
            for load_more_selector in load_more_selectors:
                try:
                    load_more_button = page.locator(load_more_selector).first
                    attempts = 0
                    max_attempts = 5  # Try to click "Load More" up to 5 times
                    
                    while attempts < max_attempts:
                        if await load_more_button.count() > 0 and await load_more_button.is_visible():
                            self.logger.info(f"Clicking load more button (attempt {attempts + 1})")
                            await load_more_button.click()
                            await page.wait_for_timeout(3000)  # Wait for new content to load
                            attempts += 1
                        else:
                            break
                    
                    if attempts > 0:
                        self.logger.info(f"Successfully clicked load more {attempts} times")
                        break
                        
                except Exception as e:
                    self.logger.debug(f"Load more selector '{load_more_selector}' failed: {e}")
                    continue
            
            # Look for pagination links (pages 2, 3, 4, etc.)
            pagination_selectors = [
                'a[href*="page="]',
                'a[href*="p="]',
                '.pagination a',
                '.pager a',
                'a:has-text("2")',
                'a:has-text("3")',
                'a:has-text("Siguiente")',
                'a:has-text(">")',
            ]
            
            for pagination_selector in pagination_selectors:
                try:
                    elements = await page.locator(pagination_selector).all()
                    if elements:
                        for element in elements:
                            href = await element.get_attribute('href')
                            if href and ('page=' in href or 'p=' in href or href.endswith('/2') or href.endswith('/3')):
                                if href.startswith('/'):
                                    href = f"https://www.bricodepot.es{href}"
                                elif not href.startswith('http'):
                                    href = response.urljoin(href)
                                if href not in pagination_links:
                                    pagination_links.append(href)
                        
                        if pagination_links:
                            self.logger.info(f"Found {len(pagination_links)} pagination links with selector: {pagination_selector}")
                            break
                            
                except Exception as e:
                    self.logger.debug(f"Pagination selector '{pagination_selector}' failed: {e}")
                    continue
            
            # Now extract product links with improved selectors
            product_selectors = [
                '.product-item a',         # Main product item links
                '.ais-Hits-item a',        # Algolia InstantSearch hits
                '.algolia-hit a',          # Algolia hit links
                '[data-objectid] a',       # Algolia object IDs
                'a[href*=".html"]',        # HTML page links (likely products)
                '.product-link',           # General product links
                '.item-link',              # Item links
                'a[href*="/productos/"]',  # Direct product links
            ]
            
            for selector in product_selectors:
                try:
                    elements = await page.locator(selector).all()
                    if elements:
                        # Extract hrefs using Playwright
                        links = []
                        for element in elements:
                            href = await element.get_attribute('href')
                            if href:
                                # Convert relative URLs to absolute
                                if href.startswith('/'):
                                    href = f"https://www.bricodepot.es{href}"
                                elif not href.startswith('http'):
                                    href = response.urljoin(href)
                                links.append(href)
                        
                        # Filter to actual product links (not category/static links)
                        filtered_links = [
                            link for link in links 
                            if link and not any(skip in link.lower() for skip in [
                                '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                                '/categoria', '/category', '/promociones', '/ofertas', '/cart',
                                '/checkout', '/account', '/search', 'identifier_brand', '/page='
                            ]) and (
                                # Accept product URLs like /espejo-clic-68-x-80-cm-8431949256265
                                '-' in link and  # Contains hyphens (typical product URLs)
                                any(char.isdigit() for char in link)  # Contains digits (often product codes)
                            )
                        ]
                        
                        if filtered_links:
                            # Remove duplicates while preserving order
                            unique_links = []
                            seen = set()
                            for link in filtered_links:
                                if link not in seen:
                                    unique_links.append(link)
                                    seen.add(link)
                            
                            product_links.extend(unique_links)
                            self.logger.info(f"Selector '{selector}' found {len(unique_links)} unique product links")
                            break
                            
                except Exception as selector_error:
                    self.logger.warning(f"Error with selector '{selector}': {selector_error}")
                    continue
            
            await page.close()
            
        except Exception as e:
            self.logger.error(f"Error processing category page {response.url}: {e}")
            return

        # Follow pagination links first (this will get us more categories with products)
        for pagination_link in pagination_links[:3]:  # Limit to first 3 pages to avoid infinite loops
            yield scrapy.Request(
                url=pagination_link,
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
                        {'method': 'wait_for_timeout', 'args': [5000]},
                    ],
                ),
            )

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
                        'timeout': 30000,
                    },
                    playwright_page_methods=[
                        {'method': 'wait_for_selector', 'args': ['body']},
                        {'method': 'wait_for_timeout', 'args': [2000]},
                    ],
                ),
            )

    async def parse_product(self, response):
        """
        Parses a product page to extract product details and sends them to the backend.

        Args:
            response (scrapy.http.Response): The response object from a product page.
        """
        product_name = None
        price = None
        description = None
        image_url = None
        
        try:
            page = response.meta["playwright_page"]
            
            # Set shorter timeouts for element extraction
            page.set_default_timeout(5000)  # 5 second timeout for all operations
            
            # Extract product name directly using Playwright
            product_name_selectors = [
                'h1.product-name',
                'h1[data-testid="product-title"]',
                '.product-item-name',
                '.product-title',
                'h1',
                '.page-title span',
                '[data-ui-id="page-title-wrapper"] h1',
            ]
            
            for selector in product_name_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        text = await element.text_content(timeout=3000)
                        if text and text.strip():
                            product_name = text.strip()
                            break
                except Exception as e:
                    self.logger.debug(f"Selector '{selector}' failed for product name: {e}")
                    continue

            # Extract price directly using Playwright
            price_selectors = [
                'span.price',
                '.price',
                '.price-wrapper .price',
                '[data-price-type="finalPrice"] .price',
                '.regular-price .price',
                '.price-container .price',
            ]
            
            for selector in price_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        price_text = await element.text_content(timeout=3000)
                        if price_text and price_text.strip():
                            # Clean price: remove spaces, non-breaking spaces, currency symbols
                            cleaned_price = price_text.strip().replace('\xa0', '').replace('€', '').replace('$', '').replace(',', '.')
                            price = cleaned_price
                            break
                except Exception as e:
                    self.logger.debug(f"Selector '{selector}' failed for price: {e}")
                    continue

            # Extract description directly using Playwright
            description_selectors = [
                'div.product-description-content p',
                '.product-info-description p',
                '.product-attribute-description',
                '.product-overview',
                '.short-description',
            ]
            
            for selector in description_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        desc_text = await element.text_content(timeout=3000)
                        if desc_text and desc_text.strip():
                            description = desc_text.strip()
                            break
                except Exception as e:
                    self.logger.debug(f"Selector '{selector}' failed for description: {e}")
                    continue

            # Extract image URL directly using Playwright
            image_selectors = [
                'img.product-image-photo',
                '.product-image-main img',
                '.fotorama__img',
                '.product-media img',
            ]
            
            for selector in image_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        src = await element.get_attribute('src', timeout=3000)
                        if src:
                            if src.startswith('/'):
                                image_url = f"https://www.bricodepot.es{src}"
                            elif not src.startswith('http'):
                                image_url = response.urljoin(src)
                            else:
                                image_url = src
                            break
                except Exception as e:
                    self.logger.debug(f"Selector '{selector}' failed for image: {e}")
                    continue
            
            await page.close()
            
        except Exception as e:
            self.logger.error(f"Error processing product page {response.url}: {e}")
            return

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
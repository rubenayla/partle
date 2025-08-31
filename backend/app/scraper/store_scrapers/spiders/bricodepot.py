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
            )

    async def parse_category(self, response):
        """
        Parses a category page to extract product links and follows them.

        Args:
            response (scrapy.http.Response): The response object from a category page.
        """
        product_links = []
        
        try:
            page = response.meta["playwright_page"]
            
            # Extract product links directly using Playwright before closing the page
            # This is more reliable than using CSS selectors on the replaced response
            product_selectors = [
                '.product-item a',         # Main product item links (WORKING!)
                'a[href*="/productos/"]',  # Direct product links
                'a[href*="/product/"]',    # Alternative product links
                '.product-item-link',      # Product item links
                '.ais-Hits-item a',        # Algolia InstantSearch hits
                '.algolia-hit a',          # Algolia hit links
                '[class*="hit"] a',        # Generic hit containers
                '[data-objectid] a',       # Algolia object IDs
                'a[href*=".html"]',        # HTML page links (likely products)
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
                                '/checkout', '/account', '/search', 'identifier_brand'
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
                            self.logger.info(f"Selector '{selector}' found {len(unique_links)} unique product links (using all)")
                            break
                            
                except Exception as selector_error:
                    self.logger.warning(f"Error with selector '{selector}': {selector_error}")
                    continue
            
            await page.close()
            
        except Exception as e:
            self.logger.error(f"Error processing category page {response.url}: {e}")
            return

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
                        'timeout': 30000,  # Reduced timeout for faster processing
                    },
                    playwright_page_methods=[
                        {'method': 'wait_for_selector', 'args': ['body']},
                        {'method': 'wait_for_timeout', 'args': [2000]},  # Reduced wait time
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
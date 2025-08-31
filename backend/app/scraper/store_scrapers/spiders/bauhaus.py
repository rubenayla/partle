"""
Scrapy spider for scraping product data from Bauhaus.

This spider navigates through categories, extracts product links, and then
scrapes detailed information for each product, including name, price,
description, and image URL. It saves this data directly to the database
using Scrapy pipelines.
"""

import scrapy
from ..items import ProductItem
from ..config import config


class BauhausSpider(scrapy.Spider):
    """
    Spider for Bauhaus website.
    """
    name = "bauhaus"
    allowed_domains = ["bauhaus.es"]
    store_id = config.STORE_IDS["bauhaus"]

    def start_requests(self):
        """
        Initiates the scraping process by sending a request to the Bauhaus homepage.
        Uses Playwright for rendering the page.
        """
        yield scrapy.Request(
            url="https://www.bauhaus.es/",
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
                    {'method': 'wait_for_timeout', 'args': [3000]},
                ],
            ),
            dont_filter=True,
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
        category_selectors = [
            'nav a[href*="/"]::attr(href)',
            '.navigation a[href*="/"]::attr(href)',
            '.main-nav a[href*="/"]::attr(href)',
            '.category-nav a[href*="/"]::attr(href)',
        ]
        
        category_links = []
        for selector in category_selectors:
            links = response.css(selector).getall()
            if links:
                # Filter for category/product pages
                valid_links = [
                    link for link in links 
                    if link and any(category in link.lower() for category in [
                        'herramientas', 'construction', 'jardin', 'ferreteria', 'tools',
                        'material', 'productos', 'categoria', 'category', 'bano', 'cocina'
                    ]) and not any(skip in link.lower() for skip in [
                        '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                        '/cuenta', '/cart', '/checkout', '/login', '/registro'
                    ])
                ]
                if valid_links:
                    category_links.extend(valid_links)
                    self.logger.info(f"Found {len(valid_links)} category links with selector: {selector}")
                    break
        
        # If no category links found, try known Bauhaus categories
        if not category_links:
            self.logger.info("No category links found, trying known categories")
            category_links = [
                "/herramientas",
                "/jardin", 
                "/construccion",
                "/bano",
                "/cocina",
                "/electricidad",
                "/pintura"
            ]
            
        for link in category_links[:3]:  # Limit to first 3 categories
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
                        {'method': 'wait_for_timeout', 'args': [3000]},
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
            '.product-item a::attr(href)',
            'a[href*="/producto/"]::attr(href)',
            'a[href*="/products/"]::attr(href)',
            '.product-link::attr(href)',
            '.product-tile a::attr(href)',
            'a[href*=".html"]::attr(href)',
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
                    ]) and (
                        # Accept product URLs with product indicators
                        '/producto/' in link.lower() or
                        '/product/' in link.lower() or
                        ('-' in link and any(char.isdigit() for char in link))
                    )
                ]
                if filtered_links:
                    product_links.extend(filtered_links[:20])  # Limit to 20 products per category
                    self.logger.info(f"Selector '{selector}' found {len(filtered_links)} valid product links (using first 20)")
                    break
        
        if not product_links:
            self.logger.info(f"No product links found on {response.url}")
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
                        {'method': 'wait_for_timeout', 'args': [3000]},
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
            'h1.product-title::text',
            'h1[data-testid="product-title"]::text',
            '.product-name h1::text',
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

        # Extract price - try multiple selectors
        price_selectors = [
            '.price-current::text',
            '.price::text',
            '.product-price .price::text',
            '[data-testid="price"]::text',
            '.price-wrapper .price::text',
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

        # Extract description - try multiple selectors
        description_selectors = [
            '.product-description p::text',
            '.product-info-description::text',
            '.product-details p::text',
            '.description::text',
        ]
        
        description = None
        for selector in description_selectors:
            desc = response.css(selector).get()
            if desc and desc.strip():
                description = desc.strip()
                break

        # Extract image URL - try multiple selectors
        image_selectors = [
            '.product-image img::attr(src)',
            '.product-media img::attr(src)',
            '.gallery-image img::attr(src)',
            'img[data-testid="product-image"]::attr(src)',
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
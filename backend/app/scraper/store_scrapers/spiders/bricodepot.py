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
        category_links = response.css('a.hm-link.main-navbar--item-parent::attr(href)').getall()
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

        # Extract product links - Bricodepot uses Algolia so products load via JS
        # Try multiple selectors for Algolia-loaded products
        product_selectors = [
            'a.product-item-link',  # Original selector
            '.ais-Hits-item a',     # Algolia InstantSearch hits
            '.algolia-hit a',       # Algolia hit links
            '[class*="hit"] a',     # Generic hit containers
            '.product-item a',      # Alternative product items
            '[data-objectid] a',    # Algolia object IDs
            '.item a[href*="/"]',   # Generic item links that go to products
        ]
        
        product_links = []
        for selector in product_selectors:
            links = response.css(f'{selector}::attr(href)').getall()
            if links:
                # Filter to actual product links (not category/static links)
                filtered_links = [
                    link for link in links 
                    if link and not any(skip in link.lower() for skip in [
                        '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                        '/categoria', '/category', '/promociones', '/ofertas'
                    ])
                ]
                if filtered_links:
                    product_links.extend(filtered_links)
                    self.logger.info(f"Selector '{selector}' found {len(filtered_links)} valid product links")
                    break
        
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

        # Extract product name
        product_name = response.css('h1.product-name::text').get()
        if product_name:
            product_name = product_name.strip()

        # Extract price and clean it (remove thousand separators, replace comma with dot)
        price = response.css('span.price::text').get()
        if price:
            # Clean price: remove spaces, non-breaking spaces, currency symbols
            price = price.strip().replace('\xa0', '').replace('€', '').replace('$', '')
            price = price.replace('.', '').replace(',', '.')  # Handle thousand separators

        # Extract description
        description = response.css('div.product-description-content p::text').get()
        if description:
            description = description.strip()

        # Extract image URL
        image_url = response.css('img.product-image-photo::attr(src)').get()

        # Create and yield the product item
        product_item = ProductItem(
            name=product_name,
            price=float(price) if price else None,
            url=response.url,
            description=description,
            image_url=image_url,
            store_id=self.store_id,
        )

        self.logger.info(f"Scraped product: {product_name}")
        yield product_item
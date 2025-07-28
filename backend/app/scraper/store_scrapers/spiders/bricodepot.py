"""
Scrapy spider for scraping product data from Brico Depot.

This spider navigates through categories, extracts product links, and then
scrapes detailed information for each product, including name, price,
description, and image URL. It then sends this data to the local backend API.
"""

import scrapy
import json
import requests

BASE_URL = "http://localhost:8000"
# TODO: This token should ideally be loaded from a secure configuration or environment variable, not hardcoded.
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMiIsImV4cCI6MTc1Mzc0MjM5M30.6gPP3p5lIVQpr74eskj9jys8p4Nwfpzrrp0kzDUz7uQ"


class BricodepotSpider(scrapy.Spider):
    """
    Spider for Brico Depot website.
    """
    name = "bricodepot"
    allowed_domains = ["bricodepot.es"]
    store_id = 4064  # BRICO DEPOT chain store ID in the backend

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
        page = response.meta["playwright_page"]
        html_content = await page.content()
        await page.close()
        response = response.replace(body=html_content, encoding='utf-8')

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
        page = response.meta["playwright_page"]
        html_content = await page.content()
        await page.close()
        response = response.replace(body=html_content, encoding='utf-8')

        # Extract product links from the category page listings
        product_links = response.css('a.product-item-link::attr(href)').getall()
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
        page = response.meta["playwright_page"]
        html_content = await page.content()
        await page.close()
        response = response.replace(body=html_content, encoding='utf-8')

        # Extract product name
        product_name = response.css('h1.product-name::text').get()
        if product_name:
            product_name = product_name.strip()

        # Extract price and clean it (remove thousand separators, replace comma with dot)
        price = response.css('span.price::text').get()
        if price:
            price = price.strip().replace('.', '').replace(',', '.')

        # Extract description
        description = response.css('div.product-description-content p::text').get()
        if description:
            description = description.strip()

        # Extract image URL
        image_url = response.css('img.product-image-photo::attr(src)').get()

        product_data = {
            'name': product_name,
            'price': float(price) if price else None,
            'url': response.url,
            'description': description,
            'image_url': image_url,
            'store_id': self.store_id,
        }

        self.logger.info(f"Sending product data: {product_data}")
        self.create_product(product_data)

    def create_product(self, product_data):
        """
        Sends the scraped product data to the backend API.

        Args:
            product_data (dict): A dictionary containing the product details.
        """
        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(f"{BASE_URL}/v1/products/", data=json.dumps(product_data), headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            self.logger.info(f"Product created successfully: {response.json()}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error creating product: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response content: {e.response.text}")
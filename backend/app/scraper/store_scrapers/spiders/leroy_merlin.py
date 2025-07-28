"""
Scrapy spider for scraping product data from Leroy Merlin.

This spider is designed to extract product details such as name, price,
description, and URL from Leroy Merlin product pages.
It uses Playwright for rendering JavaScript-heavy pages.
"""

import scrapy


class LeroyMerlinSpider(scrapy.Spider):
    """
    Spider for Leroy Merlin website.
    """
    name = "leroy_merlin"
    allowed_domains = ["leroymerlin.es"]
    start_urls = []  # This spider starts requests dynamically in start_requests

    def start_requests(self):
        """
        Initiates the scraping process by sending a request to a sample Leroy Merlin product page.
        Uses Playwright for rendering the page.
        """
        # This is a sample URL. In a real scenario, you would likely
        # crawl category pages to discover product URLs.
        yield scrapy.Request(
            url="https://www.leroymerlin.es/productos/perfil-forma-cuadrada-de-acero-en-bruto-standers-alt-25-x-an-25mm-x-l-1-m-87825775.html",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
            )
        )

    def parse(self, response):
        """
        Parses a product page to extract product details.

        Args:
            response (scrapy.http.Response): The response object from a product page.
        """
        # Extract product name
        product_name = response.css('h1.product-header-title::text').get()
        if product_name:
            product_name = product_name.strip()

        # Extract price and clean it (remove thousand separators, replace comma with dot for decimal)
        price = response.css('div.price-wrapper span.price::text').get()
        if price:
            price = price.strip().replace('.', '').replace(',', '.')

        # Extract description (this might need refinement based on actual HTML structure)
        description = response.css('div.product-description p::text').get()
        if description:
            description = description.strip()

        # Yield the extracted data as a dictionary
        yield {
            'product_name': product_name,
            'price': price,
            'description': description,
            'url': response.url,
        }
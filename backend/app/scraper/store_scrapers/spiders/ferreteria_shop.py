"""
Scrapy spider for scraping product data from Ferreteria.shop.

This spider navigates through categories, extracts product links, and then
scrapes detailed information for each product. Ferreteria.shop is a PrestaShop
platform with ~200 products focused on cabinet/kitchen hardware.
"""

import scrapy
from ..items import ProductItem
from ..config import config


class FerreteriaShopSpider(scrapy.Spider):
    """
    Spider for Ferreteria.shop website.
    """
    name = "ferreteria_shop"
    allowed_domains = ["ferreteria.shop"]
    store_id = config.STORE_IDS["ferreteria_shop"]

    def start_requests(self):
        """
        Initiates the scraping process by sending a request to the homepage.
        PrestaShop platform, no heavy JS needed.
        """
        yield scrapy.Request(
            url="https://www.ferreteria.shop/",
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response):
        """
        Parses the homepage to extract category links and follows them.
        """
        # Extract category links from navigation
        category_selectors = [
            '.category a::attr(href)',
            '.menu a::attr(href)',
            'nav a::attr(href)',
            '.top-menu a::attr(href)',
            'a[href*="/categoria/"]::attr(href)',
            'a[href*="/category/"]::attr(href)',
        ]
        
        category_links = []
        for selector in category_selectors:
            links = response.css(selector).getall()
            if links:
                # Filter for category pages
                valid_links = [
                    link for link in links 
                    if link and any(category in link.lower() for category in [
                        'herrajes', 'cocina', 'armarios', 'puertas', 'ferreteria',
                        'tiradores', 'muebles', 'categoria', 'category'
                    ]) and not any(skip in link.lower() for skip in [
                        '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                        '/cuenta', '/cart', '/checkout', '/login', '/registro'
                    ])
                ]
                if valid_links:
                    category_links.extend(valid_links)
                    self.logger.info(f"Found {len(valid_links)} category links with selector: {selector}")
                    break
        
        # Fallback: try common PrestaShop category URLs
        if not category_links:
            self.logger.info("No category links found, trying common PrestaShop patterns")
            category_links = [
                "/herrajes-armarios/",
                "/herrajes-cocina/", 
                "/herrajes-puertas/",
                "/ferreteria/",
                "/tiradores-para-muebles/"
            ]
            
        for link in category_links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_category,
                dont_filter=True,
            )

    def parse_category(self, response):
        """
        Parses a category page to extract product links and follows them.
        """
        self.logger.info(f"Parsing category: {response.url}")

        # Extract product links - Ferreteria.shop specific selectors
        product_selectors = [
            '#product_list li a::attr(href)',
            '.product-name a::attr(href)',
            'h5.product-name a::attr(href)',
            '.product-details a::attr(href)',
            'li a[href*="/"]::attr(href)',
        ]
        
        product_links = []
        for selector in product_selectors:
            links = response.css(selector).getall()
            if links:
                # Filter to actual product links - be more restrictive
                filtered_links = [
                    link for link in links 
                    if link and link.startswith(('http://www.ferreteria.shop/', 'https://www.ferreteria.shop/', '/')) 
                    and not any(skip in link.lower() for skip in [
                        '/static/', '/media/', '#', 'javascript:', 'mailto:', 'tel:',
                        '/categoria', '/category', '/cart', '/checkout', '/account',
                        '/blog', 'youtube.com', 'twitter.com', 'facebook.com', 'instagram.com'
                    ])
                    and any(product_indicator in link.lower() for product_indicator in [
                        'pernio', 'bisagra', 'tirador', 'herraje', 'cerradura', 'guia'
                    ])
                ]
                if filtered_links:
                    product_links.extend(filtered_links)
                    self.logger.info(f"Selector '{selector}' found {len(filtered_links)} valid product links")
                    break
        
        # Check for pagination
        next_page_selectors = [
            'a[rel="next"]::attr(href)',
            '.pagination a[href*="page="]::attr(href)',
            '.next::attr(href)',
            'a.next::attr(href)',
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
        """
        self.logger.info(f"Parsing product: {response.url}")

        # Extract product name - PrestaShop selectors
        product_name_selectors = [
            'h1.product-title::text',
            'h1.h1::text',
            '.product-title::text',
            'h1::text',
            '.page-title h1::text',
        ]
        
        product_name = None
        for selector in product_name_selectors:
            name = response.css(selector).get()
            if name and name.strip():
                product_name = name.strip()
                break

        # Extract price - PrestaShop selectors
        price_selectors = [
            '.current-price .price::text',
            '.price::text',
            '.product-price::text',
            '[data-field="price"]::text',
            '.precio::text',
        ]
        
        price = None
        for selector in price_selectors:
            price_text = response.css(selector).get()
            if price_text and price_text.strip():
                cleaned_price = price_text.strip().replace('\xa0', '').replace('€', '').replace('$', '').replace(',', '.')
                price = cleaned_price
                break

        # Extract description - PrestaShop selectors
        description_selectors = [
            '.product-description::text',
            '.product-description p::text',
            '.short-description::text',
            '.product-information p::text',
            '#description p::text',
        ]
        
        description = None
        for selector in description_selectors:
            desc = response.css(selector).get()
            if desc and desc.strip():
                description = desc.strip()
                break

        # Extract image URL - PrestaShop selectors
        image_selectors = [
            '.product-cover img::attr(src)',
            '.product-images img::attr(src)',
            '.js-qv-product-cover img::attr(src)',
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
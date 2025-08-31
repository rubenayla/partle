"""
Scrapy spider for scraping product data from Mengual.com.

This spider navigates through categories, extracts product links, and then
scrapes detailed information for each product, including name, price,
description, and image URL. Mengual.com uses JavaScript and lazy loading,
so this spider uses Playwright for rendering.
"""

import scrapy
import re
from ..items import ProductItem
from ..config import config


class MengualSpider(scrapy.Spider):
    """
    Spider for Mengual.com website (Spanish hardware/construction store).
    """
    name = "mengual"
    allowed_domains = ["mengual.com"]
    store_id = config.STORE_IDS.get("mengual", 4067)  # Add new store ID if needed

    def start_requests(self):
        """
        Initiates the scraping process by sending requests to main product categories.
        Uses Playwright for rendering JavaScript content.
        """
        # Start with main category pages from sitemap analysis
        category_urls = [
            "https://www.mengual.com/tiradores-y-pomos",  # Handles and knobs
            "https://www.mengual.com/bisagras",  # Hinges
            "https://www.mengual.com/guias-de-cajones",  # Drawer guides
            "https://www.mengual.com/herrajes-para-armarios",  # Closet hardware
            "https://www.mengual.com/cerraduras-y-seguridad",  # Locks
            "https://www.mengual.com/accesorios-de-cocina",  # Kitchen accessories
            "https://www.mengual.com/accesorios-de-bano",  # Bathroom accessories
            "https://www.mengual.com/herramientas-electricas",  # Power tools
            "https://www.mengual.com/herramientas-manuales",  # Hand tools
            "https://www.mengual.com/iluminacion",  # Lighting
        ]
        
        for url in category_urls:
            yield scrapy.Request(
                url=url,
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
                        {'method': 'wait_for_timeout', 'args': [3000]},  # Wait for lazy loading
                    ],
                ),
            )

    async def parse_category(self, response):
        """
        Parses a category page to extract product links and follows them.
        Handles JavaScript-loaded content and pagination.
        """
        product_links = []
        
        try:
            page = response.meta["playwright_page"]
            
            # Wait for products to load
            await page.wait_for_timeout(2000)
            
            # Scroll to trigger lazy loading
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            
            # Look for "Load More" or pagination buttons
            load_more_selectors = [
                'button:has-text("Ver más")',
                'button:has-text("Cargar más")',
                'button:has-text("Mostrar más")',
                '.load-more',
                '.btn-load-more',
                'a:has-text("Siguiente")',
            ]
            
            # Try to click load more buttons
            for selector in load_more_selectors:
                try:
                    load_more = page.locator(selector).first
                    attempts = 0
                    while attempts < 3 and await load_more.count() > 0 and await load_more.is_visible():
                        self.logger.info(f"Clicking load more button (attempt {attempts + 1})")
                        await load_more.click()
                        await page.wait_for_timeout(3000)
                        attempts += 1
                    if attempts > 0:
                        self.logger.info(f"Successfully clicked load more {attempts} times")
                        break
                except Exception as e:
                    self.logger.debug(f"Load more selector '{selector}' failed: {e}")
                    continue
            
            # Extract product links with multiple selectors
            product_selectors = [
                '.product-item a::attr(href)',
                '.product-link::attr(href)',
                'a[href*="/producto/"]::attr(href)',
                'a[href*="/product/"]::attr(href)',
                '.item-link::attr(href)',
                '.product-name a::attr(href)',
                'h3 a::attr(href)',
                'h4 a::attr(href)',
            ]
            
            for selector in product_selectors:
                try:
                    # Use Playwright to get links
                    elements = await page.locator('a').all()
                    for element in elements:
                        href = await element.get_attribute('href')
                        if href and ('/producto/' in href or '/product/' in href or 
                                   (href.startswith('/') and len(href) > 10 and '-' in href)):
                            if href.startswith('/'):
                                href = f"https://www.mengual.com{href}"
                            product_links.append(href)
                    
                    if product_links:
                        self.logger.info(f"Found {len(product_links)} product links")
                        break
                        
                except Exception as e:
                    self.logger.warning(f"Error with selector '{selector}': {e}")
                    continue
            
            await page.close()
            
        except Exception as e:
            self.logger.error(f"Error processing category page {response.url}: {e}")
            return

        # Remove duplicates and limit products per category
        unique_links = list(dict.fromkeys(product_links))[:15]  # Limit to 15 products per category
        
        if not unique_links:
            self.logger.info(f"No product links found on {response.url}")
            return
        
        self.logger.info(f"Following {len(unique_links)} unique product links from {response.url}")
        
        for link in unique_links:
            yield scrapy.Request(
                url=link,
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
        Parses a product page to extract product details.
        Handles lazy-loaded images and JavaScript content.
        """
        product_name = None
        price = None
        description = None
        image_url = None
        
        try:
            page = response.meta["playwright_page"]
            
            # Set timeout for operations
            page.set_default_timeout(5000)
            
            # Extract product name
            name_selectors = [
                'h1.product-name',
                'h1[data-ui-id="page-title-wrapper"]',
                '.product-title',
                'h1.page-title',
                'h1',
                '.product-name',
            ]
            
            for selector in name_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        text = await element.text_content(timeout=3000)
                        if text and text.strip():
                            product_name = text.strip()
                            break
                except Exception as e:
                    self.logger.debug(f"Name selector '{selector}' failed: {e}")
                    continue

            # Extract price
            price_selectors = [
                '.price',
                '.product-price .price',
                '.price-wrapper .price',
                '.special-price .price',
                '.regular-price .price',
                '[data-price-type="finalPrice"] .price',
                '.precio',
            ]
            
            for selector in price_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        price_text = await element.text_content(timeout=3000)
                        if price_text and price_text.strip():
                            # Clean price: remove currency symbols and convert to float
                            cleaned_price = re.sub(r'[^\d,.]', '', price_text.strip())
                            if cleaned_price:
                                # Handle Spanish number format (comma as decimal separator)
                                if ',' in cleaned_price and '.' in cleaned_price:
                                    # Format like 1.234,56
                                    cleaned_price = cleaned_price.replace('.', '').replace(',', '.')
                                elif ',' in cleaned_price:
                                    # Format like 123,56
                                    cleaned_price = cleaned_price.replace(',', '.')
                                price = cleaned_price
                                break
                except Exception as e:
                    self.logger.debug(f"Price selector '{selector}' failed: {e}")
                    continue

            # Extract description
            desc_selectors = [
                '.product-info-description',
                '.product-description-content',
                '.product-overview',
                '.short-description',
                '.product-details',
                '.descripcion',
            ]
            
            for selector in desc_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        desc_text = await element.text_content(timeout=3000)
                        if desc_text and desc_text.strip():
                            description = desc_text.strip()
                            break
                except Exception as e:
                    self.logger.debug(f"Description selector '{selector}' failed: {e}")
                    continue

            # Extract image URL (handle lazy loading with data-amsrc)
            image_selectors = [
                'img[data-amsrc]',  # Lazy loaded images
                '.product-image-main img',
                '.product-media img',
                '.fotorama__img',
                '.product-image img',
                'img.product-image-photo',
            ]
            
            for selector in image_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.count() > 0:
                        # Try data-amsrc first (lazy loading), then src
                        src = await element.get_attribute('data-amsrc', timeout=3000)
                        if not src:
                            src = await element.get_attribute('src', timeout=3000)
                        
                        if src and src.strip():
                            if src.startswith('//'):
                                image_url = f"https:{src}"
                            elif src.startswith('/'):
                                image_url = f"https://www.mengual.com{src}"
                            elif not src.startswith('http'):
                                image_url = response.urljoin(src)
                            else:
                                image_url = src
                            break
                except Exception as e:
                    self.logger.debug(f"Image selector '{selector}' failed: {e}")
                    continue
            
            await page.close()
            
        except Exception as e:
            self.logger.error(f"Error processing product page {response.url}: {e}")
            return

        # Convert price to float if possible
        price_float = None
        if price:
            try:
                price_float = float(price)
            except (ValueError, TypeError):
                self.logger.warning(f"Could not convert price '{price}' to float")

        # Create and yield the product item if we have basic info
        if product_name:
            product_item = ProductItem(
                name=product_name,
                price=price_float,
                url=response.url,
                description=description,
                image_url=image_url,
                store_id=self.store_id,
            )

            self.logger.info(f"Scraped Mengual product: {product_name} | Price: {price_float} | Image: {bool(image_url)}")
            yield product_item
        else:
            self.logger.warning(f"No product name found for {response.url}")
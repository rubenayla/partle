"""
Simple Mengual spider without Playwright - uses direct HTTP requests
"""

import scrapy
import re
from ..items import ProductItem
from ..config import config


class MengualSimpleSpider(scrapy.Spider):
    """
    Simplified spider for Mengual.com without JavaScript rendering.
    """
    name = "mengual_simple"
    allowed_domains = ["mengual.com"]
    store_id = config.STORE_IDS.get("mengual", 4070)

    # Real product URLs from mengual.com
    start_urls = [
        # Handles and knobs
        "https://www.mengual.com/tirador-tipo-gola-emotions-2-en-efecto-inox-negro-mate-y-blanco-mate",
        "https://www.mengual.com/tirador-embutido-cubic-rectangular",
        "https://www.mengual.com/tirador-big-quanto",
        "https://www.mengual.com/tirador-italo-redondo-plano",
        "https://www.mengual.com/tirador-kimera",
        "https://www.mengual.com/tote-cazoleta-rectangular",
        "https://www.mengual.com/tirador-gualte",
        "https://www.mengual.com/tirador-nordico-sense-mini",
    ]

    def parse(self, response):
        """Parse product page and extract product information using regex from meta tags."""
        self.logger.info(f"Parsing Mengual product: {response.url}")
        
        html_content = response.text

        # Extract product name from meta tag og:title
        name = None
        name_match = re.search(r'<meta property="og:title" content="([^"]*)"', html_content)
        if name_match:
            # Decode HTML entities
            import html
            name = html.unescape(name_match.group(1))

        # Extract price from meta tag
        price = None
        price_match = re.search(r'<meta property="product:price:amount" content="([^"]*)"', html_content)
        if price_match:
            try:
                price = float(price_match.group(1))
            except ValueError:
                price = None

        # Extract description from meta tag og:description
        description = None
        desc_match = re.search(r'<meta property="og:description" content="([^"]*)"', html_content)
        if desc_match:
            import html
            desc_text = html.unescape(desc_match.group(1))
            if desc_text.strip():
                description = desc_text.strip()
        
        # If no meta description, try regular meta description
        if not description:
            desc_match = re.search(r'<meta name="description" content="([^"]*)"', html_content)
            if desc_match:
                import html
                desc_text = html.unescape(desc_match.group(1))
                if desc_text.strip():
                    description = desc_text.strip()

        # Extract image URL from meta tag og:image
        image_url = None
        img_match = re.search(r'<meta property="og:image" content="([^"]*)"', html_content)
        if img_match:
            image_url = img_match.group(1)
            # Clean up query parameters to get base image URL
            if '?' in image_url:
                image_url = image_url.split('?')[0]

        # Create and yield the product item if we have basic info
        if name:
            product_item = ProductItem(
                name=name,
                price=price,
                url=response.url,
                description=description,
                image_url=image_url,
                store_id=self.store_id,
            )

            self.logger.info(f"Scraped Mengual product: {name} | Price: {price} | Image: {bool(image_url)}")
            yield product_item
        else:
            self.logger.warning(f"No product name found for {response.url}")
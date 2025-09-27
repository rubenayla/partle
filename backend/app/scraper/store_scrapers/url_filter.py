"""
Database-based URL filtering for scrapers.
Checks if a URL already exists in the database to avoid re-scraping.
"""

import logging
from urllib.parse import urlparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from scrapy.dupefilters import BaseDupeFilter
from .config import config

logger = logging.getLogger(__name__)


class DatabaseUrlFilter(BaseDupeFilter):
    """
    Filter URLs by checking if they already exist in the database.
    This prevents re-scraping products we already have.
    """

    def __init__(self, database_url=None):
        self.database_url = database_url or config.DATABASE_URL
        self.engine = create_engine(self.database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.checked_urls = {}  # Cache to avoid repeated DB queries
        self.stats = {
            'new_products': 0,
            'existing_products': 0,
            'categories_visited': 0
        }
        logger.info("DatabaseUrlFilter initialized")

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def _is_product_url(self, url):
        """
        Determine if a URL is a product page (should be filtered if exists)
        or a category/listing page (should always be allowed through).
        """
        # Common patterns for category/listing URLs - always crawl these
        category_indicators = [
            '/category/', '/categoria/', '/c/', '/search',
            '/buscar', '/catalog', '/catalogo', '/collection',
            '/department', '/seccion', 'page=', 'sort=',
            '/shop/', '/tienda/', '/productos/', '/all-products',
            '?page=', '&page=', '/page/', '#'
        ]

        url_lower = url.lower()

        # Check if it's a category/listing page
        for indicator in category_indicators:
            if indicator in url_lower:
                return False

        # Common patterns for product URLs
        product_indicators = [
            '/product/', '/producto/', '/p/', '/item/',
            '/articulo/', '/ref/', 'sku=', 'id=',
            '-p-', '_p_', '/dp/', '/gp/product/'
        ]

        # Check if it's likely a product page
        for indicator in product_indicators:
            if indicator in url_lower:
                return True

        # Heuristic: URLs with many path segments are often products
        path = urlparse(url).path
        segments = [s for s in path.split('/') if s]
        if len(segments) >= 3:
            return True

        return False

    def request_seen(self, request):
        """
        Check if we should filter this request.
        Returns True to filter (skip), False to process.
        """
        url = request.url

        # Check cache first
        if url in self.checked_urls:
            return self.checked_urls[url]

        # Always allow category/listing pages through
        if not self._is_product_url(url):
            self.stats['categories_visited'] += 1
            self.checked_urls[url] = False
            return False

        # For product URLs, check if they exist in database
        try:
            with self.Session() as session:
                # Check if this URL already exists for ANY store
                result = session.execute(
                    text("SELECT id FROM products WHERE url = :url LIMIT 1"),
                    {"url": url}
                ).first()

                if result:
                    # Product already exists - skip it
                    self.stats['existing_products'] += 1
                    self.checked_urls[url] = True

                    if self.stats['existing_products'] % 50 == 0:
                        logger.info(f"Skipped {self.stats['existing_products']} existing products")

                    return True
                else:
                    # New product - allow it through
                    self.stats['new_products'] += 1
                    self.checked_urls[url] = False

                    if self.stats['new_products'] % 10 == 0:
                        logger.info(f"Found {self.stats['new_products']} NEW products!")

                    return False

        except Exception as e:
            logger.error(f"Database error checking URL {url}: {e}")
            # On error, allow the URL through (better to risk a duplicate than miss new products)
            return False

    def close(self, reason):
        """Called when spider closes."""
        logger.info(
            f"Spider closed. Stats: {self.stats['new_products']} new products, "
            f"{self.stats['existing_products']} existing products skipped, "
            f"{self.stats['categories_visited']} categories visited"
        )

    def log(self, request, spider):
        """Log filtered requests if needed."""
        pass
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os
from datetime import datetime
from typing import Optional
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

# Add the backend app to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from app.db.models import Product, Store
from .config import config


class DatabasePipeline:
    """Pipeline to save scraped items to the database."""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
    
    def open_spider(self, spider):
        """Initialize database connection when spider starts."""
        try:
            self.engine = create_engine(config.DATABASE_URL, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
            spider.logger.info(f"Database connection established: {config.DATABASE_URL}")
        except Exception as e:
            spider.logger.error(f"Failed to connect to database: {e}")
            raise
    
    def close_spider(self, spider):
        """Clean up database connection when spider closes."""
        if self.engine:
            self.engine.dispose()
            spider.logger.info("Database connection closed")
    
    def process_item(self, item, spider):
        """Process each scraped item and save to database."""
        if not self.SessionLocal:
            spider.logger.error("No database connection available")
            return item
        
        db = self.SessionLocal()
        try:
            adapter = ItemAdapter(item)
            
            # Extract and validate data from item
            name = adapter.get('name')
            price = adapter.get('price')
            url = adapter.get('url')
            description = adapter.get('description')
            image_url = adapter.get('image_url')
            store_id = adapter.get('store_id')
            
            # Validate required fields
            if not name or not store_id:
                spider.logger.warning(
                    f"Skipping item with missing required fields: "
                    f"name='{name}', store_id={store_id}"
                )
                spider.crawler.stats.inc_value('pipeline/items_dropped')
                return item
            
            # Validate store exists
            store = db.query(Store).filter(Store.id == store_id).first()
            if not store:
                spider.logger.error(f"Store with ID {store_id} not found in database")
                spider.crawler.stats.inc_value('pipeline/items_dropped')
                return item
            
            # Sanitize price
            if price is not None:
                try:
                    price = float(price)
                    if price < 0:
                        spider.logger.warning(f"Negative price {price} for product '{name}', setting to None")
                        price = None
                except (ValueError, TypeError):
                    spider.logger.warning(f"Invalid price '{price}' for product '{name}', setting to None")
                    price = None
            
            # Check if product already exists by URL and store_id
            existing_product = None
            if url and config.ENABLE_DUPLICATE_FILTER:
                existing_product = db.query(Product).filter(
                    Product.url == url,
                    Product.store_id == store_id
                ).first()
            
            if existing_product and config.UPDATE_EXISTING_PRODUCTS:
                # Update existing product
                updated_fields = []
                if existing_product.name != name:
                    existing_product.name = name
                    updated_fields.append('name')
                if existing_product.price != price:
                    existing_product.price = price
                    updated_fields.append('price')
                if existing_product.description != description:
                    existing_product.description = description
                    updated_fields.append('description')
                if existing_product.image_url != image_url:
                    existing_product.image_url = image_url
                    updated_fields.append('image_url')
                
                if updated_fields:
                    existing_product.updated_at = datetime.utcnow()
                    if config.DEFAULT_CREATOR_ID:
                        existing_product.updated_by_id = config.DEFAULT_CREATOR_ID
                    
                    spider.logger.info(
                        f"Updated product '{name}' (ID: {existing_product.id}): "
                        f"fields={', '.join(updated_fields)}"
                    )
                    spider.crawler.stats.inc_value('pipeline/items_updated')
                else:
                    spider.logger.debug(f"No changes needed for product '{name}' (ID: {existing_product.id})")
                    spider.crawler.stats.inc_value('pipeline/items_unchanged')
                
            elif not existing_product:
                # Create new product
                product = Product(
                    name=name,
                    price=price,
                    url=url,
                    description=description,
                    image_url=image_url,
                    store_id=store_id,
                    creator_id=config.DEFAULT_CREATOR_ID,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(product)
                spider.logger.info(f"Created new product: '{name}'")
                spider.crawler.stats.inc_value('pipeline/items_created')
            
            else:
                spider.logger.debug(f"Duplicate product found, skipping: '{name}'")
                spider.crawler.stats.inc_value('pipeline/items_duplicate')
            
            db.commit()
            spider.crawler.stats.inc_value('pipeline/items_processed')
            
        except SQLAlchemyError as e:
            db.rollback()
            error_msg = f"Database error processing item '{adapter.get('name', 'Unknown')}': {e}"
            spider.logger.error(error_msg)
            spider.crawler.stats.inc_value('pipeline/database_errors')
            # Don't re-raise to allow spider to continue
        except Exception as e:
            db.rollback()
            error_msg = f"Unexpected error processing item '{adapter.get('name', 'Unknown')}': {e}"
            spider.logger.error(error_msg, exc_info=True)
            spider.crawler.stats.inc_value('pipeline/unexpected_errors')
            # Don't re-raise to allow spider to continue
        finally:
            db.close()
        
        return item


class StoreDeduplicationPipeline:
    """Pipeline to prevent store duplicates by name similarity."""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        
    def open_spider(self, spider):
        """Initialize database connection when spider starts."""
        try:
            self.engine = create_engine(config.DATABASE_URL, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
            spider.logger.info(f"Store deduplication pipeline initialized")
        except Exception as e:
            spider.logger.error(f"Failed to connect to database: {e}")
            raise
    
    def close_spider(self, spider):
        """Clean up database connection when spider closes."""
        if self.engine:
            self.engine.dispose()
            spider.logger.info("Store deduplication pipeline connection closed")
    
    def normalize_store_name(self, name):
        """Normalize store name for comparison."""
        if not name:
            return ""
        # Convert to lowercase, remove common variations and suffixes
        normalized = name.lower()
        normalized = normalized.replace("brico depot", "bricodepot")
        normalized = normalized.replace("brico dépôt", "bricodepot") 
        normalized = normalized.replace("brico-depot", "bricodepot")
        # Remove numbered suffixes like "_1", "_2"
        import re
        normalized = re.sub(r'_\d+$', '', normalized)
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        return normalized
    
    def process_item(self, item, spider):
        """Process store items and prevent duplicates."""
        from .items import StoreScrapersItem
        
        # Only process StoreScrapersItem (not ProductItem)
        if not isinstance(item, StoreScrapersItem):
            return item
            
        if not self.SessionLocal:
            spider.logger.error("No database connection available")
            return item
            
        adapter = ItemAdapter(item)
        store_name = adapter.get('name')
        
        if not store_name:
            spider.logger.warning("Skipping store item with no name")
            spider.crawler.stats.inc_value('store_pipeline/items_dropped')
            return item
            
        db = self.SessionLocal()
        try:
            normalized_name = self.normalize_store_name(store_name)
            
            # Check for existing stores with similar names
            existing_stores = db.query(Store).all()
            
            for existing_store in existing_stores:
                existing_normalized = self.normalize_store_name(existing_store.name)
                
                if normalized_name == existing_normalized:
                    spider.logger.info(
                        f"Duplicate store detected: '{store_name}' matches existing '{existing_store.name}' "
                        f"(ID: {existing_store.id}). Skipping."
                    )
                    spider.crawler.stats.inc_value('store_pipeline/duplicates_skipped')
                    return item
            
            # Special case: block Bricodepot variations if canonical store exists
            if "bricodepot" in normalized_name:
                canonical_store = db.query(Store).filter(Store.name == "Bricodepot").first()
                if canonical_store:
                    spider.logger.info(
                        f"Bricodepot variation '{store_name}' blocked - canonical store exists "
                        f"(ID: {canonical_store.id}). Skipping."
                    )
                    spider.crawler.stats.inc_value('store_pipeline/bricodepot_blocked')
                    return item
            
            spider.logger.info(f"Store '{store_name}' passed deduplication check")
            spider.crawler.stats.inc_value('store_pipeline/items_passed')
            
        except Exception as e:
            spider.logger.error(f"Error in store deduplication for '{store_name}': {e}")
            spider.crawler.stats.inc_value('store_pipeline/errors')
        finally:
            db.close()
            
        return item


class StoreScrapersPipeline:
    """Legacy pipeline - kept for backward compatibility."""
    def process_item(self, item, spider):
        return item

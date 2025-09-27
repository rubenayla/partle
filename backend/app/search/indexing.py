import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models import Product, Store, Tag
from app.search.client import search_client
from app.search.mappings import PRODUCT_INDEX_MAPPING

logger = logging.getLogger(__name__)

def product_to_search_doc(product: Product) -> dict:
    """Convert a Product model instance to an Elasticsearch document."""
    doc = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'spec': product.spec,
        'price': float(product.price) if product.price is not None else None,
        'url': product.url,
        'image_url': f"/v1/products/{product.id}/image" if product.image_data else None,
        'creator_id': product.creator_id,
        'created_at': product.created_at.isoformat() if product.created_at else None,
        'updated_at': product.updated_at.isoformat() if product.updated_at else None,
        'tags': [tag.name for tag in product.tags] if product.tags else []
    }
    
    # Add location if coordinates are available
    if product.lat is not None and product.lon is not None:
        doc['location'] = {
            'lat': product.lat,
            'lon': product.lon
        }
    
    # Add store information if available
    if product.store:
        doc['store_id'] = product.store.id
        doc['store_name'] = product.store.name
        doc['store_type'] = product.store.type.value if product.store.type else None
        doc['store_address'] = product.store.address
        
        # Use store location if product doesn't have its own coordinates
        if 'location' not in doc and product.store.lat is not None and product.store.lon is not None:
            doc['location'] = {
                'lat': product.store.lat,
                'lon': product.store.lon
            }
    
    return doc

def index_product(product: Product) -> bool:
    """Index a single product in Elasticsearch."""
    try:
        doc = product_to_search_doc(product)
        return search_client.index_document(str(product.id), doc)
    except Exception as e:
        logger.error(f"Error indexing product {product.id}: {e}")
        return False

def bulk_index_products(products: List[Product]) -> bool:
    """Bulk index multiple products in Elasticsearch."""
    try:
        documents = [product_to_search_doc(product) for product in products]
        return search_client.bulk_index(documents)
    except Exception as e:
        logger.error(f"Error bulk indexing products: {e}")
        return False

def delete_product_from_index(product_id: int) -> bool:
    """Remove a product from the search index."""
    try:
        return search_client.delete_document(str(product_id))
    except Exception as e:
        logger.error(f"Error deleting product {product_id} from index: {e}")
        return False

def initialize_product_index(force_recreate: bool = False) -> bool:
    """Initialize the product search index with proper mapping."""
    try:
        if not search_client.is_available():
            logger.error("Elasticsearch is not available")
            return False
        
        return search_client.create_index(PRODUCT_INDEX_MAPPING, force_recreate)
    except Exception as e:
        logger.error(f"Error initializing product index: {e}")
        return False

def reindex_all_products(db: Session, batch_size: int = 100) -> bool:
    """Reindex all products from the database."""
    try:
        # Initialize the index
        if not initialize_product_index(force_recreate=True):
            return False
        
        # Get total count
        total_products = db.query(Product).count()
        logger.info(f"Starting reindex of {total_products} products")
        
        offset = 0
        indexed_count = 0
        
        while offset < total_products:
            # Fetch batch of products with relationships
            products = (
                db.query(Product)
                .options(
                    # Eagerly load relationships to avoid N+1 queries
                    # joinedload(Product.store),
                    # joinedload(Product.tags)
                )
                .offset(offset)
                .limit(batch_size)
                .all()
            )
            
            if not products:
                break
            
            # Bulk index this batch
            if bulk_index_products(products):
                indexed_count += len(products)
                logger.info(f"Indexed batch: {indexed_count}/{total_products}")
            else:
                logger.error(f"Failed to index batch at offset {offset}")
                return False
            
            offset += batch_size
        
        logger.info(f"Successfully reindexed {indexed_count} products")
        return True
        
    except Exception as e:
        logger.error(f"Error during reindex: {e}")
        return False
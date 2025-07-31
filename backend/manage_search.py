#!/usr/bin/env python3
"""
Management script for Elasticsearch operations.
"""
import sys
import os
import logging
from sqlalchemy.orm import sessionmaker

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.api.deps import get_db
from app.search.indexing import initialize_product_index, reindex_all_products
from app.search.client import search_client

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_elasticsearch():
    """Check if Elasticsearch is available."""
    if search_client.is_available():
        logger.info("✅ Elasticsearch is available")
        return True
    else:
        logger.error("❌ Elasticsearch is not available")
        return False

def init_index(force_recreate=False):
    """Initialize the search index."""
    logger.info("Initializing product search index...")
    
    if not check_elasticsearch():
        return False
    
    success = initialize_product_index(force_recreate=force_recreate)
    
    if success:
        logger.info("✅ Search index initialized successfully")
        return True
    else:
        logger.error("❌ Failed to initialize search index")
        return False

def reindex_products():
    """Reindex all products."""
    logger.info("Starting product reindexing...")
    
    if not check_elasticsearch():
        return False
    
    # Get database session
    db = next(get_db())
    
    try:
        success = reindex_all_products(db, batch_size=100)
        
        if success:
            logger.info("✅ Product reindexing completed successfully")
            return True
        else:
            logger.error("❌ Product reindexing failed")
            return False
            
    finally:
        db.close()

def show_index_info():
    """Show information about the search index."""
    if not check_elasticsearch():
        return
    
    try:
        # Get index stats
        stats = search_client.client.indices.stats(index=search_client.index_name)
        total_docs = stats['indices'][search_client.index_name]['total']['docs']['count']
        
        logger.info(f"📊 Index: {search_client.index_name}")
        logger.info(f"📊 Total documents: {total_docs}")
        
        # Test search
        response = search_client.search({
            'query': {'match_all': {}},
            'size': 0
        })
        
        logger.info(f"📊 Search works: {response['hits']['total']['value']} documents found")
        
    except Exception as e:
        logger.error(f"❌ Error getting index info: {e}")

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python manage_search.py <command>")
        print("Commands:")
        print("  check       - Check Elasticsearch availability")
        print("  init        - Initialize search index")
        print("  init-force  - Force recreate search index")
        print("  reindex     - Reindex all products")
        print("  info        - Show index information")
        print("  setup       - Initialize index and reindex products")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check":
        check_elasticsearch()
    
    elif command == "init":
        init_index(force_recreate=False)
    
    elif command == "init-force":
        init_index(force_recreate=True)
    
    elif command == "reindex":
        reindex_products()
    
    elif command == "info":
        show_index_info()
    
    elif command == "setup":
        logger.info("🚀 Setting up search infrastructure...")
        if init_index(force_recreate=True):
            reindex_products()
            show_index_info()
        else:
            logger.error("❌ Setup failed during index initialization")
            sys.exit(1)
    
    else:
        logger.error(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
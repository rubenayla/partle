import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import Product
from app.search.client import search_client
from app.search.queries import build_product_search_query, build_product_aggregation_query
from app.search.indexing import initialize_product_index, reindex_all_products
from app.schemas import product as schema
from app.utils.test_data import get_excluded_test_tags

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/products/", response_model=Dict[str, Any])
def search_products(
    q: Optional[str] = Query(None, description="Search query"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    lat: Optional[float] = Query(None, description="Latitude for location search"),
    lon: Optional[float] = Query(None, description="Longitude for location search"),
    distance_km: Optional[float] = Query(None, description="Distance in kilometers for location search"),
    sort_by: Optional[str] = Query(None, description="Sort by: price_asc, price_desc, name_asc, created_at, distance, random"),
    include_test_data: bool = Query(False, description="Include mock/test data in results"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    include_aggregations: bool = Query(False, description="Include faceted search aggregations")
):
    """
    Search products using Elasticsearch with advanced filtering and sorting.
    Falls back to database search if Elasticsearch is unavailable.
    """
    
    # Check if Elasticsearch is available
    if not search_client.is_available():
        logger.warning("Elasticsearch unavailable, falling back to database search")
        raise HTTPException(
            status_code=503,
            detail="Search service temporarily unavailable"
        )
    
    try:
        # Parse tags
        tag_list = None
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

        # Get excluded tags for test data
        excluded_tags = None
        if not include_test_data:
            excluded_tags = get_excluded_test_tags()
        
        # Build location dict
        location = None
        if lat is not None and lon is not None:
            location = {'lat': lat, 'lon': lon}
        
        # Build search query
        search_query = build_product_search_query(
            query=q,
            min_price=min_price,
            max_price=max_price,
            tags=tag_list,
            excluded_tags=excluded_tags,
            store_id=store_id,
            location=location,
            distance_km=distance_km,
            sort_by=sort_by,
            limit=limit,
            offset=offset
        )
        
        # Execute search
        response = search_client.search(search_query)
        
        # Extract products from response
        products = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            # Convert back to the format expected by frontend
            product = {
                'id': source['id'],
                'name': source['name'],
                'description': source.get('description'),
                'spec': source.get('spec'),
                'price': source.get('price'),
                'url': source.get('url'),
                'image_url': source.get('image_url'),
                'lat': source.get('location', {}).get('lat') if source.get('location') else None,
                'lon': source.get('location', {}).get('lon') if source.get('location') else None,
                'store_id': source.get('store_id'),
                'created_at': source.get('created_at'),
                'updated_at': source.get('updated_at'),
                'updated_by_id': source.get('creator_id'),  # Map for compatibility
                'tags': [{'name': tag} for tag in source.get('tags', [])]  # Convert to expected format
            }
            products.append(product)
        
        result = {
            'products': products,
            'total': response['hits']['total']['value'],
            'limit': limit,
            'offset': offset
        }
        
        # Add aggregations if requested
        if include_aggregations:
            agg_query = build_product_aggregation_query(query=q)
            agg_response = search_client.search(agg_query)
            
            result['aggregations'] = {
                'price_ranges': agg_response.get('aggregations', {}).get('price_ranges', {}),
                'tags': agg_response.get('aggregations', {}).get('tags', {}),
                'store_types': agg_response.get('aggregations', {}).get('store_types', {})
            }
        
        return result
        
    except Exception as e:
        logger.error(f"Error in product search: {e}")
        raise HTTPException(
            status_code=500,
            detail="Search request failed"
        )

@router.post("/products/reindex")
def reindex_products(
    force: bool = Query(False, description="Force recreate index"),
    db: Session = Depends(get_db)
):
    """
    Reindex all products in Elasticsearch.
    This is an admin operation that should be protected in production.
    """
    
    if not search_client.is_available():
        raise HTTPException(
            status_code=503,
            detail="Elasticsearch is not available"
        )
    
    try:
        success = reindex_all_products(db, batch_size=100)
        
        if success:
            total_count = db.query(Product).count()
            return {
                'success': True,
                'message': f'Successfully reindexed {total_count} products',
                'total_products': total_count
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Reindexing failed"
            )
            
    except Exception as e:
        logger.error(f"Error during reindex: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Reindexing failed: {str(e)}"
        )

@router.post("/products/init-index")
def initialize_index(
    force_recreate: bool = Query(False, description="Force recreate index")
):
    """
    Initialize the product search index.
    """
    
    if not search_client.is_available():
        raise HTTPException(
            status_code=503,
            detail="Elasticsearch is not available"
        )
    
    try:
        success = initialize_product_index(force_recreate=force_recreate)
        
        if success:
            return {
                'success': True,
                'message': 'Product index initialized successfully'
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Index initialization failed"
            )
            
    except Exception as e:
        logger.error(f"Error initializing index: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Index initialization failed: {str(e)}"
        )

@router.get("/health")
def search_health():
    """Check search service health."""
    return {
        'elasticsearch_available': search_client.is_available(),
        'index_name': search_client.index_name,
        'host': f"{search_client.host}:{search_client.port}"
    }
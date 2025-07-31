from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def build_product_search_query(
    query: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    tags: Optional[List[str]] = None,
    store_id: Optional[int] = None,
    location: Optional[Dict[str, float]] = None,
    distance_km: Optional[float] = None,
    sort_by: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> Dict[str, Any]:
    """Build an Elasticsearch query for product search."""
    
    # Start with match_all if no query
    if not query:
        es_query = {'match_all': {}}
    else:
        # Multi-match query across name and description with different boosts
        es_query = {
            'bool': {
                'should': [
                    # Exact match on name gets highest boost
                    {
                        'match': {
                            'name': {
                                'query': query,
                                'boost': 3.0
                            }
                        }
                    },
                    # Partial match on name with ngrams
                    {
                        'match': {
                            'name.ngram': {
                                'query': query,
                                'boost': 2.0
                            }
                        }
                    },
                    # Match in description
                    {
                        'match': {
                            'description': {
                                'query': query,
                                'boost': 1.0
                            }
                        }
                    },
                    # Match in description with ngrams
                    {
                        'match': {
                            'description.ngram': {
                                'query': query,
                                'boost': 0.5
                            }
                        }
                    },
                    # Match in store name
                    {
                        'match': {
                            'store_name': {
                                'query': query,
                                'boost': 1.5
                            }
                        }
                    }
                ],
                'minimum_should_match': 1
            }
        }
    
    # Build filters
    filters = []
    
    # Price range filter
    if min_price is not None or max_price is not None:
        price_filter = {'range': {'price': {}}}
        if min_price is not None:
            price_filter['range']['price']['gte'] = min_price
        if max_price is not None:
            price_filter['range']['price']['lte'] = max_price
        filters.append(price_filter)
    
    # Tags filter
    if tags:
        filters.append({'terms': {'tags': tags}})
    
    # Store filter
    if store_id is not None:
        filters.append({'term': {'store_id': store_id}})
    
    # Location filter
    if location and distance_km:
        filters.append({
            'geo_distance': {
                'distance': f'{distance_km}km',
                'location': {
                    'lat': location['lat'],
                    'lon': location['lon']
                }
            }
        })
    
    # Combine query and filters
    if filters:
        if query:
            full_query = {
                'bool': {
                    'must': [es_query],
                    'filter': filters
                }
            }
        else:
            full_query = {
                'bool': {
                    'must': [es_query],
                    'filter': filters
                }
            }
    else:
        full_query = es_query
    
    # Build sort
    sort_options = []
    if sort_by == 'price_asc':
        sort_options.append({'price': {'order': 'asc', 'missing': '_last'}})
    elif sort_by == 'price_desc':
        sort_options.append({'price': {'order': 'desc', 'missing': '_last'}})
    elif sort_by == 'name_asc':
        sort_options.append({'name.raw': {'order': 'asc'}})
    elif sort_by == 'created_at':
        sort_options.append({'created_at': {'order': 'desc'}})
    elif sort_by == 'created_at_asc':
        sort_options.append({'created_at': {'order': 'asc'}})
    elif sort_by == 'random':
        sort_options.append({'_script': {
            'type': 'number',
            'script': 'Math.random()',
            'order': 'desc'
        }})
    elif location and sort_by == 'distance':
        sort_options.append({
            '_geo_distance': {
                'location': {
                    'lat': location['lat'],
                    'lon': location['lon']
                },
                'order': 'asc',
                'unit': 'km'
            }
        })
    else:
        # Default relevance sort, but add random for tie-breaking
        if query:
            sort_options.append('_score')
        sort_options.append({'_script': {
            'type': 'number',
            'script': 'Math.random()',
            'order': 'desc'
        }})
    
    # Build the complete search body
    search_body = {
        'query': full_query,
        'from': offset,
        'size': limit,
        '_source': True  # Return all source fields
    }
    
    if sort_options:
        search_body['sort'] = sort_options
    
    return search_body

def build_product_suggest_query(query: str, limit: int = 5) -> Dict[str, Any]:
    """Build a suggestion query for product search autocomplete."""
    return {
        'suggest': {
            'product_suggest': {
                'prefix': query,
                'completion': {
                    'field': 'name.completion',
                    'size': limit
                }
            }
        }
    }

def build_product_aggregation_query(
    query: Optional[str] = None,
    existing_filters: Optional[Dict] = None
) -> Dict[str, Any]:
    """Build query for faceted search aggregations."""
    
    # Base query
    if query:
        base_query = build_product_search_query(query=query, limit=0)['query']
    else:
        base_query = {'match_all': {}}
    
    return {
        'query': base_query,
        'size': 0,  # We only want aggregations
        'aggs': {
            'price_ranges': {
                'range': {
                    'field': 'price',
                    'ranges': [
                        {'to': 10},
                        {'from': 10, 'to': 50},
                        {'from': 50, 'to': 100},
                        {'from': 100, 'to': 500},
                        {'from': 500}
                    ]
                }
            },
            'tags': {
                'terms': {
                    'field': 'tags',
                    'size': 20
                }
            },
            'store_types': {
                'terms': {
                    'field': 'store_type',
                    'size': 10
                }
            }
        }
    }
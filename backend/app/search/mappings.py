PRODUCT_INDEX_MAPPING = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0,
        'analysis': {
            'analyzer': {
                'product_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'stop',
                        'snowball',
                        'asciifolding'
                    ]
                },
                'ngram_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',  
                    'filter': [
                        'lowercase',
                        'product_ngram',
                        'asciifolding'
                    ]
                }
            },
            'filter': {
                'product_ngram': {
                    'type': 'ngram',
                    'min_gram': 2,
                    'max_gram': 3
                }
            }
        }
    },
    'mappings': {
        'properties': {
            'id': {
                'type': 'integer'
            },
            'name': {
                'type': 'text',
                'analyzer': 'product_analyzer',
                'fields': {
                    'raw': {
                        'type': 'keyword'
                    },
                    'ngram': {
                        'type': 'text',
                        'analyzer': 'ngram_analyzer'
                    }
                }
            },
            'description': {
                'type': 'text',
                'analyzer': 'product_analyzer',
                'fields': {
                    'ngram': {
                        'type': 'text',
                        'analyzer': 'ngram_analyzer'
                    }
                }
            },
            'spec': {
                'type': 'text',
                'analyzer': 'product_analyzer'
            },
            'price': {
                'type': 'float'
            },
            'url': {
                'type': 'keyword',
                'index': False
            },
            'image_url': {
                'type': 'keyword',
                'index': False
            },
            'location': {
                'type': 'geo_point'
            },
            'store_id': {
                'type': 'integer'
            },
            'store_name': {
                'type': 'text',
                'analyzer': 'product_analyzer',
                'fields': {
                    'raw': {
                        'type': 'keyword'
                    }
                }
            },
            'store_type': {
                'type': 'keyword'
            },
            'store_address': {
                'type': 'text',
                'analyzer': 'product_analyzer'
            },
            'tags': {
                'type': 'keyword'
            },
            'creator_id': {
                'type': 'integer'
            },
            'created_at': {
                'type': 'date'
            },
            'updated_at': {
                'type': 'date'
            }
        }
    }
}

STORE_INDEX_MAPPING = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0,
        'analysis': {
            'analyzer': {
                'store_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'stop',
                        'snowball',
                        'asciifolding'
                    ]
                }
            }
        }
    },
    'mappings': {
        'properties': {
            'id': {
                'type': 'integer'
            },
            'name': {
                'type': 'text',
                'analyzer': 'store_analyzer',
                'fields': {
                    'raw': {
                        'type': 'keyword'
                    }
                }
            },
            'type': {
                'type': 'keyword'
            },
            'address': {
                'type': 'text',
                'analyzer': 'store_analyzer'
            },
            'location': {
                'type': 'geo_point'
            },
            'homepage': {
                'type': 'keyword',
                'index': False
            },
            'tags': {
                'type': 'keyword'
            },
            'owner_id': {
                'type': 'integer'
            }
        }
    }
}
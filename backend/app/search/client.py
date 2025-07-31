import os
import logging
from typing import Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

logger = logging.getLogger(__name__)

class SearchClient:
    def __init__(self):
        self._client: Optional[Elasticsearch] = None
        self.host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
        self.port = int(os.getenv('ELASTICSEARCH_PORT', 9200))
        self.index_name = os.getenv('ELASTICSEARCH_INDEX', 'products')
        
    @property
    def client(self) -> Elasticsearch:
        if self._client is None:
            self._client = Elasticsearch(
                [{'host': self.host, 'port': self.port, 'scheme': 'http'}],
                request_timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )
        return self._client
    
    def is_available(self) -> bool:
        try:
            info = self.client.info()
            logger.info(f"Elasticsearch cluster info: {info['cluster_name']}")
            return True
        except ConnectionError as e:
            logger.warning(f"Elasticsearch not available: {e}")
            return False
        except Exception as e:
            logger.error(f"Error checking Elasticsearch availability: {e}")
            return False
    
    def create_index(self, mapping: dict, force_recreate: bool = False) -> bool:
        try:
            if force_recreate and self.client.indices.exists(index=self.index_name):
                self.client.indices.delete(index=self.index_name)
                logger.info(f"Deleted existing index: {self.index_name}")
            
            if not self.client.indices.exists(index=self.index_name):
                response = self.client.indices.create(
                    index=self.index_name,
                    body=mapping
                )
                logger.info(f"Created index: {self.index_name} with response: {response}")
                return True
            else:
                logger.info(f"Index {self.index_name} already exists")
                return True
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return False
    
    def index_document(self, doc_id: str, document: dict) -> bool:
        try:
            response = self.client.index(
                index=self.index_name,
                id=doc_id,
                body=document
            )
            logger.debug(f"Indexed document {doc_id}: {response['result']}")
            return True
        except Exception as e:
            logger.error(f"Error indexing document {doc_id}: {e}")
            return False
    
    def bulk_index(self, documents: list) -> bool:
        if not documents:
            return True
            
        try:
            body = []
            for doc in documents:
                body.append({
                    'index': {
                        '_index': self.index_name,
                        '_id': doc['id']
                    }
                })
                body.append(doc)
            
            response = self.client.bulk(body=body)
            
            if response.get('errors'):
                for item in response['items']:
                    if 'index' in item and item['index'].get('error'):
                        logger.error(f"Bulk index error: {item['index']['error']}")
                return False
            
            logger.info(f"Bulk indexed {len(documents)} documents")
            return True
        except Exception as e:
            logger.error(f"Error bulk indexing: {e}")
            return False
    
    def search(self, query: dict) -> dict:
        try:
            response = self.client.search(
                index=self.index_name,
                body=query
            )
            return response
        except NotFoundError:
            logger.warning(f"Index {self.index_name} not found")
            return {'hits': {'hits': [], 'total': {'value': 0}}}
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return {'hits': {'hits': [], 'total': {'value': 0}}}
    
    def delete_document(self, doc_id: str) -> bool:
        try:
            response = self.client.delete(
                index=self.index_name,
                id=doc_id,
                ignore=[404]
            )
            logger.debug(f"Deleted document {doc_id}: {response.get('result', 'not_found')}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            return False

# Global search client instance
search_client = SearchClient()
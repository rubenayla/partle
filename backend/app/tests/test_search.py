import pytest
import time
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.models import Product, Store, Tag, User
from app.search.client import search_client
from app.search.indexing import (
    index_product, 
    bulk_index_products, 
    delete_product_from_index,
    initialize_product_index,
    product_to_search_doc
)
from app.search.queries import build_product_search_query


class TestElasticsearchIntegration:
    """Integration tests for Elasticsearch search functionality."""
    
    @pytest.fixture(autouse=True)
    def setup_test_index(self):
        """Set up a clean test index before each test."""
        if search_client.is_available():
            # Use test index
            search_client.index_name = "test_products"
            # Clean up any existing test index
            try:
                search_client.client.indices.delete(index="test_products")
            except:
                pass
            # Initialize fresh index
            initialize_product_index(force_recreate=True)
            time.sleep(1)  # Allow ES to process
        yield
        # Cleanup after test
        if search_client.is_available():
            try:
                search_client.client.indices.delete(index="test_products")
            except:
                pass
            # Reset to default index name
            search_client.index_name = "products"

    def test_elasticsearch_availability(self):
        """Test that Elasticsearch is available for testing."""
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available for testing")
        
        assert search_client.is_available()
        info = search_client.client.info()
        assert "cluster_name" in info

    def test_index_initialization(self):
        """Test that search index can be created properly."""
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available")
        
        success = initialize_product_index(force_recreate=True)
        assert success
        
        # Verify index exists
        assert search_client.client.indices.exists(index=search_client.index_name)

    def test_product_to_search_doc_conversion(self, sample_product_with_store):
        """Test conversion of Product model to Elasticsearch document."""
        product, store = sample_product_with_store
        
        doc = product_to_search_doc(product)
        
        assert doc['id'] == product.id
        assert doc['name'] == product.name
        assert doc['description'] == product.description
        assert doc['price'] == float(product.price) if product.price else None
        assert doc['store_id'] == product.store_id
        assert doc['store_name'] == store.name if store else None
        
        if product.lat and product.lon:
            assert doc['location']['lat'] == product.lat
            assert doc['location']['lon'] == product.lon

    def test_single_product_indexing(self, sample_product_with_store):
        """Test indexing a single product."""
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available")
        
        product, _ = sample_product_with_store
        
        success = index_product(product)
        assert success
        
        # Wait for indexing
        time.sleep(1)
        
        # Verify document exists
        response = search_client.search({
            'query': {'term': {'id': product.id}},
            'size': 1
        })
        
        assert response['hits']['total']['value'] == 1
        assert response['hits']['hits'][0]['_source']['name'] == product.name

    def test_bulk_product_indexing(self, sample_products):
        """Test bulk indexing multiple products."""
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available")
        
        products = sample_products
        
        success = bulk_index_products(products)
        assert success
        
        # Wait for indexing
        time.sleep(1)
        
        # Verify all documents exist
        response = search_client.search({
            'query': {'match_all': {}},
            'size': len(products)
        })
        
        assert response['hits']['total']['value'] == len(products)

    def test_product_deletion_from_index(self, sample_product_with_store):
        """Test removing a product from search index."""
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available")
        
        product, _ = sample_product_with_store
        
        # First index the product
        index_product(product)
        time.sleep(1)
        
        # Then delete it
        success = delete_product_from_index(product.id)
        assert success
        
        time.sleep(1)
        
        # Verify it's gone
        response = search_client.search({
            'query': {'term': {'id': product.id}},
            'size': 1
        })
        
        assert response['hits']['total']['value'] == 0


class TestSearchEndpoints:
    """Test the FastAPI search endpoints."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_search_health_endpoint(self):
        """Test the search health check endpoint."""
        response = self.client.get("/v1/search/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "elasticsearch_available" in data
        assert "index_name" in data
        assert "host" in data

    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_products_endpoint_basic(self):
        """Test basic product search endpoint."""
        response = self.client.get("/v1/search/products/")
        assert response.status_code == 200
        
        data = response.json()
        assert "products" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert isinstance(data["products"], list)

    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_products_with_query(self):
        """Test product search with query parameter."""
        response = self.client.get("/v1/search/products/?q=test")
        assert response.status_code == 200
        
        data = response.json()
        assert "products" in data
        # Should return products matching "test"

    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_products_with_filters(self):
        """Test product search with price and other filters."""
        params = {
            "min_price": 10,
            "max_price": 100,
            "sort_by": "price_asc",
            "limit": 5
        }
        
        response = self.client.get("/v1/search/products/", params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["products"]) <= 5

    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_products_with_aggregations(self):
        """Test product search with aggregations."""
        response = self.client.get("/v1/search/products/?include_aggregations=true")
        assert response.status_code == 200
        
        data = response.json()
        assert "aggregations" in data
        assert "price_ranges" in data["aggregations"]
        assert "tags" in data["aggregations"]

    def test_search_unavailable_fallback(self):
        """Test behavior when Elasticsearch is unavailable."""
        with patch.object(search_client, 'is_available', return_value=False):
            response = self.client.get("/v1/search/products/")
            assert response.status_code == 503
            assert "temporarily unavailable" in response.json()["detail"].lower()


class TestSearchQueries:
    """Test search query building logic."""
    
    def test_basic_query_building(self):
        """Test building basic search queries."""
        query = build_product_search_query(query="test product")
        
        assert "query" in query
        assert "from" in query
        assert "size" in query
        assert query["from"] == 0
        assert query["size"] == 20

    def test_query_with_filters(self):
        """Test building queries with filters."""
        query = build_product_search_query(
            query="test",
            min_price=10,
            max_price=100,
            tags=["electronics", "gadgets"],
            sort_by="price_asc"
        )
        
        assert "sort" in query
        assert any("price" in str(sort_item) for sort_item in query["sort"])

    def test_query_with_location(self):
        """Test building queries with geographic filters."""
        query = build_product_search_query(
            location={"lat": 40.7128, "lon": -74.0060},
            distance_km=10,
            sort_by="distance"
        )
        
        # Should include geo_distance filter and distance sorting
        query_str = str(query)
        assert "geo_distance" in query_str or "_geo_distance" in query_str

    def test_empty_query(self):
        """Test building query without search term."""
        query = build_product_search_query()
        
        # Should default to match_all
        assert "match_all" in str(query["query"])


class TestProductCRUDSync:
    """Test that CRUD operations sync with Elasticsearch."""
    
    def setup_method(self):
        """Set up test client and mock Elasticsearch."""
        self.client = TestClient(app)
        self.mock_es = MagicMock()

    def test_product_creation_triggers_indexing(self, authenticated_headers, sample_user):
        """Test that creating a product triggers Elasticsearch indexing."""
        with patch.object(search_client, 'is_available', return_value=True), \
             patch('app.search.indexing.index_product') as mock_index:
            
            product_data = {
                "name": "Test Product for Indexing",
                "description": "This should be indexed",
                "price": 25.99
            }
            
            response = self.client.post(
                "/v1/products/",
                json=product_data,
                headers=authenticated_headers
            )
            
            assert response.status_code == 201
            mock_index.assert_called_once()

    def test_product_update_triggers_reindexing(self, authenticated_headers, sample_product):
        """Test that updating a product triggers Elasticsearch reindexing."""
        with patch.object(search_client, 'is_available', return_value=True), \
             patch('app.search.indexing.index_product') as mock_index:
            
            update_data = {
                "name": "Updated Product Name",
                "description": "Updated description"
            }
            
            response = self.client.patch(
                f"/v1/products/{sample_product.id}",
                json=update_data,
                headers=authenticated_headers
            )
            
            assert response.status_code == 200
            mock_index.assert_called_once()

    def test_product_deletion_removes_from_index(self, authenticated_headers, sample_product):
        """Test that deleting a product removes it from Elasticsearch."""
        with patch.object(search_client, 'is_available', return_value=True), \
             patch('app.search.indexing.delete_product_from_index') as mock_delete:
            
            response = self.client.delete(
                f"/v1/products/{sample_product.id}",
                headers=authenticated_headers
            )
            
            assert response.status_code == 204
            mock_delete.assert_called_once_with(sample_product.id)

    def test_add_tag_triggers_reindexing(self, authenticated_headers, sample_product, sample_tag):
        """Test that adding tags to a product triggers reindexing."""
        with patch.object(search_client, 'is_available', return_value=True), \
             patch('app.search.indexing.index_product') as mock_index:
            
            response = self.client.post(
                f"/v1/products/{sample_product.id}/tags/{sample_tag.id}",
                headers=authenticated_headers
            )
            
            assert response.status_code == 201
            mock_index.assert_called_once()


# Additional fixtures for testing
@pytest.fixture
def sample_user(db):
    """Create a sample user for testing."""
    from app.db.models import User
    
    user = User(
        email="test@example.com",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def sample_product_with_store(db, sample_user):
    """Create a sample product with store for testing."""
    from app.db.models import Store, StoreType
    
    store = Store(
        name="Test Store",
        type=StoreType.physical,
        lat=40.7128,
        lon=-74.0060,
        address="123 Test St, New York, NY",
        owner_id=sample_user.id
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    
    product = Product(
        name="Test Product with Store", 
        description="A test product for search testing",
        price=19.99,
        store_id=store.id,
        creator_id=sample_user.id,
        updated_by_id=sample_user.id,
        lat=40.7138,
        lon=-74.0050
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product, store

@pytest.fixture
def sample_products(db, sample_user):
    """Create multiple sample products for bulk testing."""
    products = []
    
    for i in range(5):
        product = Product(
            name=f"Test Product {i}",
            description=f"Test description for product {i}",
            price=10.0 + i,
            creator_id=sample_user.id,
            updated_by_id=sample_user.id
        )
        db.add(product)
        products.append(product)
    
    db.commit()
    
    for product in products:
        db.refresh(product)
    
    return products

@pytest.fixture
def sample_product(db, sample_user):
    """Create a single sample product for testing."""
    product = Product(
        name="Sample Product",
        description="A sample product for testing",
        price=15.99,
        creator_id=sample_user.id,
        updated_by_id=sample_user.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@pytest.fixture
def sample_tag(db):
    """Create a sample tag for testing."""
    tag = Tag(name="test-tag")
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@pytest.fixture
def authenticated_headers(sample_user):
    """Create authentication headers for testing."""
    # Mock authentication for testing
    return {"Authorization": "Bearer mock-token"}
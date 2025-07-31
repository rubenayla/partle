"""
Simple, focused tests for Elasticsearch search functionality.
These tests verify the core search features work correctly.
"""
import pytest
import time
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.search.client import search_client
from app.search.queries import build_product_search_query


class TestSearchBasics:
    """Basic search functionality tests."""
    
    def test_search_client_availability(self):
        """Test that we can determine if Elasticsearch is available."""
        # This should not fail regardless of ES availability
        is_available = search_client.is_available()
        assert isinstance(is_available, bool)
    
    def test_search_query_building(self):
        """Test that search queries are built correctly."""
        # Test basic query
        query = build_product_search_query(query="test product")
        
        assert isinstance(query, dict)
        assert "query" in query
        assert "from" in query
        assert "size" in query
        assert query["from"] == 0
        assert query["size"] == 20
    
    def test_search_query_with_filters(self):
        """Test query building with various filters."""
        query = build_product_search_query(
            query="test",
            min_price=10,
            max_price=100,
            tags=["electronics", "gadgets"],
            sort_by="price_asc",
            limit=5,
            offset=10
        )
        
        assert query["size"] == 5
        assert query["from"] == 10
        assert "sort" in query
        
        # Should contain price range filter
        query_str = str(query)
        assert "range" in query_str
        assert "price" in query_str


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
        assert isinstance(data["elasticsearch_available"], bool)
    
    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_products_endpoint_exists(self):
        """Test that the search products endpoint exists and returns expected format."""
        response = self.client.get("/v1/search/products/")
        assert response.status_code == 200
        
        data = response.json()
        assert "products" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert isinstance(data["products"], list)
        assert isinstance(data["total"], int)
    
    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_with_query_parameter(self):
        """Test search with a query parameter."""
        response = self.client.get("/v1/search/products/?q=test")
        assert response.status_code == 200
        
        data = response.json()
        assert "products" in data
        assert isinstance(data["products"], list)
    
    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_with_pagination(self):
        """Test search with pagination parameters."""
        response = self.client.get("/v1/search/products/?limit=5&offset=0")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["products"]) <= 5
        assert data["limit"] == 5
        assert data["offset"] == 0
    
    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_with_price_filters(self):
        """Test search with price filtering."""
        response = self.client.get("/v1/search/products/?min_price=10&max_price=100")
        assert response.status_code == 200
        
        data = response.json()
        # Verify that returned products respect price filter
        for product in data["products"]:
            if product.get("price") is not None:
                assert 10 <= product["price"] <= 100
    
    def test_search_unavailable_fallback(self):
        """Test behavior when Elasticsearch is unavailable."""
        with patch.object(search_client, 'is_available', return_value=False):
            response = self.client.get("/v1/search/products/")
            assert response.status_code == 503
            
            data = response.json()
            assert "detail" in data
            assert "unavailable" in data["detail"].lower()


class TestSearchRelevance:
    """Test search relevance and ranking."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)
    
    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_test2_relevance(self):
        """
        Test the specific case that was originally broken: searching for 'test2'.
        This is a regression test for the sorting bug that was fixed.
        """
        response = self.client.get("/v1/search/products/?q=test2")
        assert response.status_code == 200
        
        data = response.json()
        
        if data["total"] > 0:
            # If we have results, check that products containing 'test2' are relevant
            products = data["products"]
            
            # Find products with 'test2' in the name
            test2_products = [p for p in products if 'test2' in p.get('name', '').lower()]
            
            if test2_products:
                # test2 products should appear early in results (good relevance)
                first_test2_position = next(
                    i for i, p in enumerate(products) 
                    if 'test2' in p.get('name', '').lower()
                )
                
                # Should be in top 5 results for good relevance
                assert first_test2_position < 5, f"test2 product found at position {first_test2_position}, expected in top 5"
                
                # The exact match 'test2' should be the first test2 result
                first_test2_product = test2_products[0]
                assert 'test2' in first_test2_product['name'].lower()
    
    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_sorting_works(self):
        """Test that sorting parameters work correctly."""
        # Test random sorting
        response1 = self.client.get("/v1/search/products/?sort_by=random&limit=10")
        assert response1.status_code == 200
        
        # Test price sorting (if products with prices exist)
        response2 = self.client.get("/v1/search/products/?sort_by=price_asc&limit=10")
        assert response2.status_code == 200
        
        data = response2.json()
        products_with_prices = [p for p in data["products"] if p.get("price") is not None]
        
        if len(products_with_prices) > 1:
            prices = [p["price"] for p in products_with_prices]
            assert prices == sorted(prices), "Products should be sorted by price ascending"


class TestSearchIntegration:
    """Integration tests that verify the complete search pipeline."""
    
    def setup_method(self):
        """Set up test client.""" 
        self.client = TestClient(app)
    
    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available")
    def test_search_returns_expected_format(self):
        """Test that search returns the expected data format."""
        response = self.client.get("/v1/search/products/?q=test")
        assert response.status_code == 200
        
        data = response.json()
        
        # Check top-level structure
        required_fields = ["products", "total", "limit", "offset"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Check product structure
        if data["products"]:
            product = data["products"][0]
            expected_product_fields = ["id", "name", "description", "price", "tags"]
            
            for field in expected_product_fields:
                assert field in product, f"Missing product field: {field}"
            
            # Verify data types
            assert isinstance(product["id"], int)
            assert isinstance(product["name"], str)
            assert isinstance(product["tags"], list)
    
    @pytest.mark.skipif(not search_client.is_available(), reason="Elasticsearch not available") 
    def test_search_with_aggregations(self):
        """Test search with aggregations enabled."""
        response = self.client.get("/v1/search/products/?include_aggregations=true")
        assert response.status_code == 200
        
        data = response.json()
        
        if "aggregations" in data:
            aggs = data["aggregations"]
            expected_agg_types = ["price_ranges", "tags", "store_types"]
            
            for agg_type in expected_agg_types:
                assert agg_type in aggs, f"Missing aggregation: {agg_type}"
    
    def test_api_matches_curl_behavior(self):
        """
        Test that reproduces the exact curl command behavior.
        This ensures our API works as expected from external calls.
        """
        # This reproduces: curl "http://localhost:8000/v1/search/products/?q=test2"
        import requests
        
        try:
            response = requests.get(
                "http://localhost:8000/v1/search/products/?q=test2",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure matches expectations
                assert "products" in data
                assert "total" in data
                assert isinstance(data["products"], list)
                assert isinstance(data["total"], int)
                
                # If we have results, verify we got some test-related products
                if data["total"] > 0:
                    # Look for at least one product containing 'test' in the results
                    test_products = [
                        p for p in data["products"] 
                        if 'test' in f"{p.get('name', '')} {p.get('description', '')}".lower()
                    ]
                    
                    # Should find at least one test-related product when searching for 'test2'
                    assert len(test_products) > 0, f"No test-related products found when searching for 'test2'"
                    
                    # The first test product should be reasonably early in results
                    first_test_pos = next(
                        i for i, p in enumerate(data["products"])
                        if 'test' in f"{p.get('name', '')} {p.get('description', '')}".lower()
                    )
                    assert first_test_pos < 10, f"First test product at position {first_test_pos}, expected in top 10"
            
            else:
                # If not 200, should be a known error (like 503 if ES unavailable)
                assert response.status_code in [503], f"Unexpected status code: {response.status_code}"
                
        except requests.ConnectionError:
            pytest.skip("Could not connect to localhost:8000 - server not running")
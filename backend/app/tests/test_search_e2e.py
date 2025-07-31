"""
End-to-end tests for the complete Elasticsearch search pipeline.
These tests validate the exact workflow from product creation to search results.
"""
import pytest
import time
import requests
from fastapi.testclient import TestClient

from app.main import app
from app.search.client import search_client
from app.search.indexing import initialize_product_index, reindex_all_products


class TestSearchEndToEnd:
    """End-to-end tests that mirror real user workflows."""
    
    @pytest.fixture(autouse=True)
    def setup_test_environment(self, db_session):
        """Set up a clean test environment."""
        # Use test index to avoid conflicts
        original_index = search_client.index_name
        search_client.index_name = "test_e2e_products"
        
        if search_client.is_available():
            # Clean up any existing test index
            try:
                search_client.client.indices.delete(index="test_e2e_products")
            except:
                pass
            
            # Initialize fresh index
            initialize_product_index(force_recreate=True)
            time.sleep(2)  # Allow ES to fully initialize
        
        yield db_session
        
        # Cleanup
        if search_client.is_available():
            try:
                search_client.client.indices.delete(index="test_e2e_products")
            except:
                pass
        
        search_client.index_name = original_index

    def test_complete_search_workflow(self, authenticated_headers):
        """
        Test the complete workflow that caused the original issue:
        1. Create a product named 'test2'
        2. Verify it's indexed in Elasticsearch
        3. Search for it via API endpoint
        4. Verify search returns the product with proper relevance
        """
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available for E2E testing")
        
        client = TestClient(app)
        
        # Step 1: Create a product named 'test2' (reproducing user's scenario)
        product_data = {
            "name": "test2",
            "description": "test2",
            "price": None
        }
        
        create_response = client.post(
            "/v1/products/",
            json=product_data,
            headers=authenticated_headers
        )
        
        assert create_response.status_code == 201
        created_product = create_response.json()
        product_id = created_product["id"]
        
        # Step 2: Wait for indexing to complete
        time.sleep(2)
        
        # Verify the product is in Elasticsearch
        es_response = search_client.search({
            "query": {"term": {"id": product_id}},
            "size": 1
        })
        
        assert es_response["hits"]["total"]["value"] == 1
        indexed_doc = es_response["hits"]["hits"][0]["_source"]
        assert indexed_doc["name"] == "test2"
        assert indexed_doc["id"] == product_id
        
        # Step 3: Search via the API endpoint (reproducing user's curl command)
        search_response = client.get("/v1/search/products/?q=test2")
        
        assert search_response.status_code == 200
        search_data = search_response.json()
        
        # Step 4: Verify search results
        assert "products" in search_data
        assert search_data["total"] >= 1
        
        # Find our test2 product in the results
        test2_products = [p for p in search_data["products"] if p["name"] == "test2"]
        assert len(test2_products) == 1
        
        found_product = test2_products[0]
        assert found_product["id"] == product_id
        assert found_product["name"] == "test2"
        assert found_product["description"] == "test2"
        
        # Step 5: Test relevance - 'test2' should be the first result
        first_result = search_data["products"][0]
        assert first_result["name"] == "test2", f"Expected 'test2' first, got '{first_result['name']}'"

    def test_search_with_multiple_test_products(self, authenticated_headers):
        """
        Test search behavior with multiple 'test' products to verify relevance scoring.
        """
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available for E2E testing")
        
        client = TestClient(app)
        
        # Create multiple test products
        test_products = [
            {"name": "test1", "description": "first test product"},
            {"name": "test2", "description": "second test product"},  
            {"name": "test3", "description": "third test product"},
            {"name": "TEST PRODUCT", "description": "uppercase test product"},
            {"name": "other product", "description": "contains test in description"}
        ]
        
        created_ids = []
        for product_data in test_products:
            response = client.post(
                "/v1/products/",
                json=product_data,
                headers=authenticated_headers
            )
            assert response.status_code == 201
            created_ids.append(response.json()["id"])
        
        # Wait for indexing
        time.sleep(3)
        
        # Search for 'test2' specifically
        search_response = client.get("/v1/search/products/?q=test2")
        assert search_response.status_code == 200
        
        results = search_response.json()
        assert results["total"] >= len(test_products)
        
        # Verify 'test2' is the first result (highest relevance)
        first_result = results["products"][0]
        assert "test2" in first_result["name"].lower()
        
        # Search for 'test' broadly
        broad_search = client.get("/v1/search/products/?q=test")
        assert broad_search.status_code == 200
        
        broad_results = broad_search.json()
        assert broad_results["total"] >= len(test_products)
        
        # All our test products should be in the results
        found_names = [p["name"] for p in broad_results["products"]]
        for product_data in test_products:
            assert any(product_data["name"] in name for name in found_names)

    def test_search_sorting_and_filtering(self, authenticated_headers):
        """Test advanced search features like sorting and filtering."""
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available for E2E testing") 
        
        client = TestClient(app)
        
        # Create products with different prices
        products_with_prices = [
            {"name": "expensive test", "description": "pricey", "price": 100.0},
            {"name": "cheap test", "description": "affordable", "price": 10.0},
            {"name": "medium test", "description": "reasonable", "price": 50.0}
        ]
        
        for product_data in products_with_prices:
            response = client.post(
                "/v1/products/",
                json=product_data,
                headers=authenticated_headers
            )
            assert response.status_code == 201
        
        time.sleep(2)
        
        # Test price filtering
        price_filter_response = client.get(
            "/v1/search/products/?q=test&min_price=20&max_price=80"
        )
        assert price_filter_response.status_code == 200
        
        filtered_results = price_filter_response.json()
        for product in filtered_results["products"]:
            if product.get("price"):
                assert 20 <= product["price"] <= 80
        
        # Test sorting by price
        price_sort_response = client.get(
            "/v1/search/products/?q=test&sort_by=price_asc"
        )
        assert price_sort_response.status_code == 200
        
        sorted_results = price_sort_response.json()
        prices = [p["price"] for p in sorted_results["products"] if p.get("price")]
        assert prices == sorted(prices)  # Should be in ascending order

    def test_search_fallback_behavior(self):
        """Test that search gracefully falls back when Elasticsearch is unavailable."""
        client = TestClient(app)
        
        # Mock Elasticsearch as unavailable
        with pytest.MonkeyPatch().context() as m:
            m.setattr(search_client, 'is_available', lambda: False)
            
            response = client.get("/v1/search/products/?q=test")
            
            # Should return 503 Service Unavailable
            assert response.status_code == 503
            assert "temporarily unavailable" in response.json()["detail"].lower()

    def test_product_crud_elasticsearch_sync(self, authenticated_headers):
        """
        Test that CRUD operations properly sync with Elasticsearch.
        This prevents regressions in the indexing pipeline.
        """
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available for E2E testing")
        
        client = TestClient(app)
        
        # 1. Create a product
        product_data = {
            "name": "CRUD Test Product",
            "description": "Testing CRUD sync",
            "price": 29.99
        }
        
        create_response = client.post(
            "/v1/products/",
            json=product_data,
            headers=authenticated_headers
        )
        assert create_response.status_code == 201
        
        product_id = create_response.json()["id"]
        time.sleep(1)
        
        # Verify it's indexed
        search_response = client.get(f"/v1/search/products/?q=CRUD Test Product")
        assert search_response.status_code == 200
        assert search_response.json()["total"] >= 1
        
        # 2. Update the product
        update_data = {
            "name": "Updated CRUD Test Product",
            "description": "Updated description"
        }
        
        update_response = client.patch(
            f"/v1/products/{product_id}",
            json=update_data,
            headers=authenticated_headers
        )
        assert update_response.status_code == 200
        time.sleep(1)
        
        # Verify the update is reflected in search
        updated_search = client.get("/v1/search/products/?q=Updated CRUD")
        assert updated_search.status_code == 200
        assert updated_search.json()["total"] >= 1
        
        # Old name should not be found
        old_search = client.get("/v1/search/products/?q=CRUD Test Product")
        old_results = old_search.json()
        # Should either find no results or not find the exact old name
        exact_matches = [p for p in old_results["products"] 
                        if p["name"] == "CRUD Test Product"]
        assert len(exact_matches) == 0
        
        # 3. Delete the product
        delete_response = client.delete(
            f"/v1/products/{product_id}",
            headers=authenticated_headers
        )
        assert delete_response.status_code == 204
        time.sleep(1)
        
        # Verify it's removed from search
        final_search = client.get("/v1/search/products/?q=Updated CRUD")
        final_results = final_search.json()
        
        # Should not find the deleted product
        found_deleted = [p for p in final_results["products"] 
                        if p["id"] == product_id]
        assert len(found_deleted) == 0

    @pytest.mark.slow
    def test_reindex_command_functionality(self, db_session):
        """Test the management command for reindexing all products."""
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available for E2E testing")
        
        # This test validates that the reindex command works
        # as the user experienced it
        
        # Get count of products in database
        from app.db.models import Product
        db_product_count = db_session.query(Product).count()
        
        if db_product_count == 0:
            pytest.skip("No products in database to test reindexing")
        
        # Run reindex
        success = reindex_all_products(db_session, batch_size=10)
        assert success
        
        time.sleep(2)
        
        # Verify all products are now in Elasticsearch
        es_response = search_client.search({
            "query": {"match_all": {}},
            "size": 0  # Just get count
        })
        
        es_product_count = es_response["hits"]["total"]["value"]
        assert es_product_count == db_product_count, \
            f"Expected {db_product_count} products in ES, found {es_product_count}"

    def test_search_api_matches_curl_command(self):
        """
        Test that reproduces the exact curl command the user ran.
        This is a regression test for the original issue.
        """
        if not search_client.is_available():
            pytest.skip("Elasticsearch not available for E2E testing")
        
        # This reproduces: curl "http://localhost:8000/v1/search/products/?q=test2"
        import requests
        
        try:
            response = requests.get(
                "http://localhost:8000/v1/search/products/?q=test2",
                timeout=5
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert "products" in data
            assert "total" in data
            assert isinstance(data["products"], list)
            
            # If we found results, verify they contain 'test' in name or description
            if data["total"] > 0:
                for product in data["products"]:
                    product_text = f"{product.get('name', '')} {product.get('description', '')}".lower()
                    assert "test" in product_text, f"Product {product} doesn't contain 'test'"
            
        except requests.ConnectionError:
            pytest.skip("Could not connect to localhost:8000 - server not running")
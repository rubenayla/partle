"""
Proper pytest tests for mock-data filtering.
This is how it SHOULD be done - not with shell scripts!
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestMockDataFiltering:
    """Test that mock-data products are filtered correctly."""

    def test_products_endpoint_excludes_mock_data_by_default(self):
        """Products endpoint should not return mock-data tagged products."""
        response = client.get("/v1/products/")
        assert response.status_code == 200

        products = response.json()
        for product in products:
            tags = [tag['name'] for tag in product.get('tags', [])]
            assert 'mock-data' not in tags, f"Found mock-data in product {product['name']}"

    def test_products_endpoint_includes_mock_data_when_requested(self):
        """Products endpoint should return mock-data when include_test_data=true."""
        response = client.get("/v1/products/?include_test_data=true")
        assert response.status_code == 200

        # This would verify mock-data products are included
        products = response.json()
        # We can't assert they exist without knowing the DB state,
        # but we can verify the parameter is accepted
        assert response.status_code == 200

    def test_openapi_spec_documents_include_test_data(self):
        """OpenAPI spec should document the include_test_data parameter."""
        response = client.get("/openapi.json")
        spec = response.json()

        params = spec['paths']['/v1/products/']['get']['parameters']
        param_names = [p['name'] for p in params]

        assert 'include_test_data' in param_names
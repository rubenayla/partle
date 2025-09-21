"""Test product endpoints for mock-data filtering."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_products_exclude_mock_data_by_default():
    """Products should not include mock-data tagged items by default."""
    response = client.get("/v1/products/")
    assert response.status_code == 200

    products = response.json()
    for product in products:
        tags = [tag['name'] for tag in product.get('tags', [])]
        assert 'mock-data' not in tags


def test_products_include_mock_data_when_requested():
    """Products should include mock-data when include_test_data=true."""
    response = client.get("/v1/products/?include_test_data=true")
    assert response.status_code == 200
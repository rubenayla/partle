"""
Simple end-to-end tests for MCP bridge endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_mcp_health():
    """Test that MCP health endpoint works."""
    response = client.get("/v1/mcp/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["servers_available"] == 6


def test_mcp_servers_list():
    """Test that MCP servers list returns expected servers."""
    response = client.get("/v1/mcp/servers")
    assert response.status_code == 200
    data = response.json()

    # Check basic structure
    assert "servers" in data
    assert len(data["servers"]) == 6

    # Check first server has required fields
    first_server = data["servers"][0]
    assert first_server["name"] == "partle-products"
    assert "capabilities" in first_server
    assert "endpoint" in first_server


def test_mcp_manifest():
    """Test that MCP manifest returns valid structure for ChatGPT."""
    response = client.get("/v1/mcp/manifest")
    assert response.status_code == 200
    data = response.json()

    # Check manifest structure
    assert data["version"] == "1.0.0"
    assert data["name"] == "Partle MCP Services"
    assert "servers" in data
    assert "endpoints" in data

    # Check endpoints are listed
    endpoints = data["endpoints"]
    assert endpoints["discovery"] == "/v1/mcp/servers"
    assert endpoints["manifest"] == "/v1/mcp/manifest"


def test_mcp_execute_products():
    """Test executing a product search through MCP."""
    request_data = {
        "server": "partle-products",
        "method": "search_products",
        "params": {"query": "", "limit": 5},
        "id": 123
    }

    response = client.post("/v1/mcp/execute/partle-products", json=request_data)
    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "result" in data
    assert data["id"] == 123


def test_mcp_execute_invalid_server():
    """Test that invalid server returns 404."""
    request_data = {
        "server": "invalid-server",
        "method": "test",
        "params": {},
        "id": 1
    }

    response = client.post("/v1/mcp/execute/invalid-server", json=request_data)
    assert response.status_code == 404


def test_mcp_execute_invalid_method():
    """Test that invalid method returns 400."""
    request_data = {
        "server": "partle-products",
        "method": "invalid_method",
        "params": {},
        "id": 1
    }

    response = client.post("/v1/mcp/execute/partle-products", json=request_data)
    assert response.status_code == 400
    assert "Unknown method" in response.json()["detail"]
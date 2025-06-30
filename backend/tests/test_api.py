import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.v1 import parts, stores, auth, tags, products
from app.auth import security
from app.db.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency override


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[parts.get_db] = override_get_db
app.dependency_overrides[stores.get_db] = override_get_db
app.dependency_overrides[auth.get_db] = override_get_db
app.dependency_overrides[tags.get_db] = override_get_db
app.dependency_overrides[security.get_db] = override_get_db
app.dependency_overrides[products.get_db] = override_get_db

client = TestClient(app)


def test_get_parts_empty():
    response = client.get("/v1/parts/")
    assert response.status_code == 200
    assert response.json() == []


def test_login_unknown_email():
    resp = client.post(
        "/v1/auth/login",
        data={"username": "missing@example.com", "password": "x"},
    )
    assert resp.status_code == 404


def test_create_store_and_part():
    # register and authenticate user
    reg_payload = {"email": "user@example.com", "password": "secret"}
    client.post("/v1/auth/register", json=reg_payload)
    login_resp = client.post(
        "/v1/auth/login",
        data={"username": reg_payload["email"], "password": reg_payload["password"]},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    me_resp = client.get("/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200

    # create store
    store_data = {"name": "Test Store", "lat": 0.0, "lon": 0.0, "type": "physical"}
    store_resp = client.post("/v1/stores/", json=store_data, headers=headers)
    assert store_resp.status_code == 201
    store_id = store_resp.json()["id"]

    # create part associated with store
    part_data = {
        "name": "Widget",
        "sku": "W-1",
        "stock": 5,
        "price": 1.0,
        "store_id": store_id,
    }
    part_resp = client.post("/v1/parts/", json=part_data)
    assert part_resp.status_code == 201
    part_json = part_resp.json()
    assert part_json["name"] == "Widget"

    # list parts
    parts_resp = client.get("/v1/parts/")
    assert parts_resp.status_code == 200
    parts_list = parts_resp.json()
    assert len(parts_list) == 1
    assert parts_list[0]["name"] == "Widget"


def test_create_and_link_tags():
    # register and authenticate user
    reg_payload = {"email": "user2@example.com", "password": "secret"}
    client.post("/v1/auth/register", json=reg_payload)
    login_resp = client.post(
        "/v1/auth/login",
        data={"username": reg_payload["email"], "password": reg_payload["password"]},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create store
    store_data = {"name": "Test Store 2", "lat": 0.0, "lon": 0.0, "type": "physical"}
    store_resp = client.post("/v1/stores/", json=store_data, headers=headers)
    assert store_resp.status_code == 201
    store_id = store_resp.json()["id"]

    # create product
    product_data = {
        "name": "Test Product",
        "description": "A product for testing",
        "store_id": store_id,
    }
    product_resp = client.post("/v1/products/", json=product_data, headers=headers)
    assert product_resp.status_code == 201
    product_id = product_resp.json()["id"]

    # create tag
    tag_data = {"name": "Test Tag"}
    tag_resp = client.post("/v1/tags/", json=tag_data, headers=headers)
    assert tag_resp.status_code == 201
    tag_id = tag_resp.json()["id"]

    # link tag to product
    link_resp = client.post(
        f"/v1/products/{product_id}/tags/{tag_id}", headers=headers
    )
    assert link_resp.status_code == 201

    # get product and verify tag
    product_resp = client.get(f"/v1/products/{product_id}", headers=headers)
    assert product_resp.status_code == 200
    product_json = product_resp.json()
    assert len(product_json["tags"]) == 1
    assert product_json["tags"][0]["name"] == "Test Tag"


def test_create_and_link_tag_to_store():
    # register and authenticate user
    reg_payload = {"email": "user3@example.com", "password": "secret"}
    client.post("/v1/auth/register", json=reg_payload)
    login_resp = client.post(
        "/v1/auth/login",
        data={"username": reg_payload["email"], "password": reg_payload["password"]},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create store
    store_data = {"name": "Test Store 3", "lat": 0.0, "lon": 0.0, "type": "physical"}
    store_resp = client.post("/v1/stores/", json=store_data, headers=headers)
    assert store_resp.status_code == 201
    store_id = store_resp.json()["id"]

    # create tag
    tag_data = {"name": "Test Tag 2"}
    tag_resp = client.post("/v1/tags/", json=tag_data, headers=headers)
    assert tag_resp.status_code == 201
    tag_id = tag_resp.json()["id"]

    # link tag to store
    link_resp = client.post(
        f"/v1/stores/{store_id}/tags/{tag_id}", headers=headers
    )
    assert link_resp.status_code == 201

    # get store and verify tag
    store_resp = client.get(f"/v1/stores/{store_id}", headers=headers)
    assert store_resp.status_code == 200
    store_json = store_resp.json()
    assert len(store_json["tags"]) == 1
    assert store_json["tags"][0]["name"] == "Test Tag 2"

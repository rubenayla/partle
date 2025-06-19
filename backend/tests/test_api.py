import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.v1 import parts, stores, auth
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
app.dependency_overrides[security.get_db] = override_get_db

client = TestClient(app)


def test_get_parts_empty():
    response = client.get("/v1/parts/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_store_and_part():
    # register and authenticate user
    reg_payload = {"email": "user@example.com", "password": "secret"}
    client.post("/auth/register", json=reg_payload)
    login_resp = client.post(
        "/auth/login",
        data={"username": reg_payload["email"], "password": reg_payload["password"]},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

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

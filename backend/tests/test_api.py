import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.v1 import parts, stores
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

client = TestClient(app)


def test_get_parts_empty():
    response = client.get("/v1/parts/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_store_and_part():
    # create store
    store_data = {"name": "Test Store", "lat": 0.0, "lon": 0.0}
    store_resp = client.post("/v1/stores/", json=store_data)
    assert store_resp.status_code == 200
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
    assert part_resp.status_code == 200
    part_json = part_resp.json()
    assert part_json["name"] == "Widget"

    # list parts
    parts_resp = client.get("/v1/parts/")
    assert parts_resp.status_code == 200
    parts_list = parts_resp.json()
    assert len(parts_list) == 1
    assert parts_list[0]["name"] == "Widget"

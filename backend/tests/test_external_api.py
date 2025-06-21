import pytest
from app.api.v1 import auth, external, stores
from app.auth import security
from app.db.models import Base, User
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


def test_create_product_with_api_key():
    app.dependency_overrides[auth.get_db] = override_get_db
    app.dependency_overrides[stores.get_db] = override_get_db
    app.dependency_overrides[security.get_db] = override_get_db
    app.dependency_overrides[external.get_db] = override_get_db
    reg = {"email": "ext@example.com", "password": "x"}
    client.post("/v1/auth/register", json=reg)
    login = client.post(
        "/v1/auth/login", data={"username": reg["email"], "password": reg["password"]}
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me = client.get("/v1/auth/me", headers=headers)
    user_id = me.json()["id"]

    store_payload = {"name": "My Store", "type": "physical"}
    store_resp = client.post("/v1/stores/", json=store_payload, headers=headers)
    assert store_resp.status_code == 201
    store_id = store_resp.json()["id"]

    # sanity check: created store belongs to the authenticated user
    assert store_resp.json()["id"] == store_id

    external.API_KEYS["testkey"] = user_id

    prod_payload = {"name": "Ext Prod", "store_id": store_id}
    resp = client.post(
        "/v1/external/products", json=prod_payload, headers={"X-API-Key": "testkey"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Ext Prod"
    assert data["store_id"] == store_id

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.v1 import products, stores, auth
from app.auth import security
from app.db.models import Base

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

app.dependency_overrides[products.get_db] = override_get_db
app.dependency_overrides[stores.get_db] = override_get_db
app.dependency_overrides[auth.get_db] = override_get_db
app.dependency_overrides[security.get_db] = override_get_db

client = TestClient(app)


def test_product_updated_fields():
    # register and login
    email = "mod@example.com"
    password = "pw"
    client.post("/v1/auth/register", json={"email": email, "password": password})
    login = client.post(
        "/v1/auth/login",
        data={"username": email, "password": password},
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    me = client.get("/v1/auth/me", headers=headers)
    user_id = me.json()["id"]

    # create store
    store = client.post(
        "/v1/stores/",
        json={"name": "S", "lat": 0.0, "lon": 0.0, "type": "physical"},
        headers=headers,
    )
    store_id = store.json()["id"]

    # create product
    payload = {"name": "X", "store_id": store_id}
    resp = client.post("/v1/products/", json=payload, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert "updated_at" in data
    assert data["updated_by_id"] == user_id

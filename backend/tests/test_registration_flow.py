import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api.v1 import auth, parts, stores
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


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override dependencies
app.dependency_overrides[auth.get_db] = override_get_db
app.dependency_overrides[parts.get_db] = override_get_db
app.dependency_overrides[stores.get_db] = override_get_db
app.dependency_overrides[security.get_db] = override_get_db

client = TestClient(app)


def test_register_and_login_email_password():
    """User can register and login using email + password."""
    email = "foo@example.com"
    password = "barbaz"
    resp = client.post("/v1/auth/register", json={"email": email, "password": password})
    assert resp.status_code == 200

    login = client.post(
        "/v1/auth/login",
        data={"username": email, "password": password},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert token

    me = client.get("/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == email


@pytest.mark.xfail(reason="Logout endpoint not implemented")
def test_logout_then_login_again():
    email = "bar@example.com"
    password = "bazqux"
    client.post("/v1/auth/register", json={"email": email, "password": password})
    login = client.post(
        "/v1/auth/login", data={"username": email, "password": password}
    )
    token = login.json()["access_token"]

    # hypothetical logout
    out = client.post("/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert out.status_code == 204

    # should still be able to login again using remember token/cookie
    login2 = client.post(
        "/v1/auth/login",
        data={"username": email, "password": password, "remember": "1"},
    )
    assert login2.status_code == 200


def test_delete_account():
    email = "deleteme@example.com"
    password = "secret"
    client.post("/v1/auth/register", json={"email": email, "password": password})
    login = client.post(
        "/v1/auth/login", data={"username": email, "password": password}
    )
    token = login.json()["access_token"]

    delete = client.delete(
        "/v1/auth/account", headers={"Authorization": f"Bearer {token}"}
    )
    assert delete.status_code == 204

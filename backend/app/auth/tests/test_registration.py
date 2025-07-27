import pytest


def test_register_and_login_email_password(client, db):
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


def test_logout_then_login_again(client, db):
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


def test_delete_account(client, db):
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

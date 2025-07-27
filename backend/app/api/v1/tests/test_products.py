import pytest


def test_product_updated_fields(client, db):
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


def test_update_product_changes_name_and_updater(client, db):
    """PATCH /v1/products/{id} updates fields and updated_by_id."""
    # creator user and product
    creator = {"email": "creator@example.com", "password": "creds"}
    client.post("/v1/auth/register", json=creator)
    login = client.post("/v1/auth/login", data={"username": creator["email"], "password": creator["password"]})
    creator_token = login.json()["access_token"]
    creator_headers = {"Authorization": f"Bearer {creator_token}"}
    store = client.post(
        "/v1/stores/",
        json={"name": "C", "lat": 0.0, "lon": 0.0, "type": "physical"},
        headers=creator_headers,
    )
    store_id = store.json()["id"]
    product = client.post(
        "/v1/products/",
        json={"name": "Prod", "store_id": store_id},
        headers=creator_headers,
    )
    product_id = product.json()["id"]

    # updater user
    updater = {"email": "updater@example.com", "password": "pw2"}
    client.post("/v1/auth/register", json=updater)
    login2 = client.post("/v1/auth/login", data={"username": updater["email"], "password": updater["password"]})
    updater_token = login2.json()["access_token"]
    headers = {"Authorization": f"Bearer {updater_token}"}
    me = client.get("/v1/auth/me", headers=headers)
    updater_id = me.json()["id"]

    # patch product
    patch_resp = client.patch(
        f"/v1/products/{product_id}",
        json={"name": "Prod2"},
        headers=headers,
    )
    assert patch_resp.status_code == 200
    data = patch_resp.json()
    assert data["name"] == "Prod2"
    assert data["updated_by_id"] == updater_id


def test_update_product_not_found(client, db):
    """PATCH with unknown product id returns 404."""
    user = {"email": "nouser@example.com", "password": "pw"}
    client.post("/v1/auth/register", json=user)
    login = client.post("/v1/auth/login", data={"username": user["email"], "password": user["password"]})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.patch("/v1/products/999", json={"name": "whatever"}, headers=headers)
    assert resp.status_code == 404

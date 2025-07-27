import pytest
from app.api.v1 import external


def test_create_product_with_api_key(client, db):
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

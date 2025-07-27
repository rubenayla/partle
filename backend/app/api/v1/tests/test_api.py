import pytest


def test_get_parts_empty(client, db):
    response = client.get("/v1/parts/")
    assert response.status_code == 200
    assert response.json() == []


def test_login_unknown_email(client, db):
    resp = client.post(
        "/v1/auth/login",
        data={"username": "missing@example.com", "password": "x"},
    )
    assert resp.status_code == 404


def test_login_incorrect_password(client, db):
    # register user
    reg_payload = {"email": "user6@example.com", "password": "secret"}
    client.post("/v1/auth/register", json=reg_payload)

    # attempt login with incorrect password
    resp = client.post(
        "/v1/auth/login",
        data={"username": "user6@example.com", "password": "wrong-password"},
    )
    assert resp.status_code == 401
    assert "Incorrect email or password" in resp.json()["detail"]


def test_create_store_and_part(client, db):
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


def test_create_and_link_tags(client, db):
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


def test_create_and_link_tag_to_store(client, db):
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


def test_delete_product(client, db):
    # register and authenticate user
    reg_payload = {"email": "user4@example.com", "password": "secret"}
    client.post("/v1/auth/register", json=reg_payload)
    login_resp = client.post(
        "/v1/auth/login",
        data={"username": reg_payload["email"], "password": reg_payload["password"]},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create store
    store_data = {"name": "Test Store 4", "lat": 0.0, "lon": 0.0, "type": "physical"}
    store_resp = client.post("/v1/stores/", json=store_data, headers=headers)
    assert store_resp.status_code == 201
    store_id = store_resp.json()["id"]

    # create product
    product_data = {
        "name": "Test Product 2",
        "description": "A product for testing deletion",
        "store_id": store_id,
    }
    product_resp = client.post("/v1/products/", json=product_data, headers=headers)
    assert product_resp.status_code == 201
    product_id = product_resp.json()["id"]

    # delete product
    delete_resp = client.delete(f"/v1/products/{product_id}", headers=headers)
    assert delete_resp.status_code == 204

    # verify product is deleted
    get_resp = client.get(f"/v1/products/{product_id}", headers=headers)
    assert get_resp.status_code == 404


def test_delete_store(client, db):
    # register and authenticate user
    reg_payload = {"email": "user5@example.com", "password": "secret"}
    client.post("/v1/auth/register", json=reg_payload)
    login_resp = client.post(
        "/v1/auth/login",
        data={"username": reg_payload["email"], "password": reg_payload["password"]},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create store
    store_data = {"name": "Test Store 5", "lat": 0.0, "lon": 0.0, "type": "physical"}
    store_resp = client.post("/v1/stores/", json=store_data, headers=headers)
    assert store_resp.status_code == 201
    store_id = store_resp.json()["id"]

    # delete store
    delete_resp = client.delete(f"/v1/stores/{store_id}", headers=headers)
    assert delete_resp.status_code == 204

    # verify store is deleted
    get_resp = client.get(f"/v1/stores/{store_id}", headers=headers)
    assert get_resp.status_code == 404

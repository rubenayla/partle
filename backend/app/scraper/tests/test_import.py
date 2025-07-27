import pytest
import unittest.mock
import json
import sys # Keep sys for import_ferreterias

from app.db.models import StoreType
from app.scraper.import_ferreterias import import_stores, SCRAPED_DATA_FILE, BASE_URL, LOGIN_URL, STORES_URL, EMAIL, PASSWORD




@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(client, db): # Use client and db from conftest
    # Register and authenticate a user for tests requiring authentication
    reg_payload = {"email": "test_user@example.com", "password": "test_password"}
    client.post("/v1/auth/register", json=reg_payload)
    login_resp = client.post(
        "/v1/auth/login",
        data={"username": reg_payload["email"], "password": reg_payload["password"]},
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return client, headers


def test_create_store_physical_enum(authenticated_client, client, db):
    client, headers = authenticated_client
    store_data = {"name": "Physical Store", "lat": 1.0, "lon": 1.0, "type": "physical"}
    store_resp = client.post("/v1/stores/", json=store_data, headers=headers)
    assert store_resp.status_code == 201
    assert store_resp.json()["type"] == "physical"


def test_create_store_online_enum(authenticated_client, client, db):
    client, headers = authenticated_client
    store_data = {"name": "Online Store", "lat": 2.0, "lon": 2.0, "type": "online"}
    store_resp = client.post("/v1/stores/", json=store_data, headers=headers)
    assert store_resp.status_code == 201
    assert store_resp.json()["type"] == "online"


def test_create_store_chain_enum(authenticated_client, client, db):
    client, headers = authenticated_client
    store_data = {"name": "Chain Store", "lat": 3.0, "lon": 3.0, "type": "chain"}
    store_resp = client.post("/v1/stores/", json=store_data, headers=headers)
    assert store_resp.status_code == 201
    assert store_resp.json()["type"] == "chain"





@pytest.fixture
def mock_requests():
    with unittest.mock.patch('requests.post') as mock_post, \
         unittest.mock.patch('requests.get') as mock_get, \
         unittest.mock.patch('os.path.exists') as mock_exists, \
         unittest.mock.patch('builtins.open', unittest.mock.mock_open()) as mock_open:
        yield mock_post, mock_get, mock_exists, mock_open


def test_import_stores_skips_exact_duplicates(mock_requests, client, db):
    mock_post, mock_get, mock_exists, mock_open = mock_requests

    # Mock login success
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"access_token": "fake_token"}

    # Mock existing stores (one exact duplicate)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "Existing Store", "address": "123 Main St", "lat": 40.0, "lon": -3.0, "type": "physical"}
    ]

    # Mock scraped data (one exact duplicate, one new)
    mock_exists.return_value = True
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps([
        {"name": "Existing Store", "address": "123 Main St", "latitude": 40.0, "longitude": -3.0, "website": "", "phone": ""},
        {"name": "New Store", "address": "456 Oak Ave", "latitude": 41.0, "longitude": -4.0, "website": "", "phone": ""}
    ])

    import_stores()

    # Verify login was called
    mock_post.assert_any_call(LOGIN_URL, data={"username": EMAIL, "password": PASSWORD})

    # Verify existing stores were fetched
    mock_get.assert_called_with(STORES_URL, headers={"Authorization": "Bearer fake_token"})

    # Verify only the new store was attempted to be added
    assert mock_post.call_count == 2  # One for login, one for the new store
    mock_post.assert_called_with(STORES_URL, headers=unittest.mock.ANY, json={
        "name": "New Store",
        "type": "physical",
        "address": "456 Oak Ave",
        "lat": 41.0,
        "lon": -4.0,
        "homepage": ""
    })


def test_import_stores_suffixes_name_duplicates(mock_requests, client, db):
    mock_post, mock_get, mock_exists, mock_open = mock_requests

    # Mock login success
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"access_token": "fake_token"}

    # Mock existing stores (one with a name that will be duplicated)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "Duplicate Name", "address": "123 Main St", "lat": 40.0, "lon": -3.0, "type": "physical"}
    ]

    # Mock scraped data (one with the same name but different details)
    mock_exists.return_value = True
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps([
        {"name": "Duplicate Name", "address": "456 Oak Ave", "latitude": 41.0, "longitude": -4.0, "website": "", "phone": ""}
    ])

    import_stores()

    # Verify the new store was added with a suffixed name
    assert mock_post.call_count == 2  # One for login, one for the new store
    mock_post.assert_called_with(STORES_URL, headers=unittest.mock.ANY, json={
        "name": "Duplicate Name_1",
        "type": "physical",
        "address": "456 Oak Ave",
        "lat": 41.0,
        "lon": -4.0,
        "homepage": ""
    })


def test_import_stores_handles_multiple_name_duplicates(mock_requests, client, db):
    mock_post, mock_get, mock_exists, mock_open = mock_requests

    # Mock login success
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"access_token": "fake_token"}

    # Mock existing stores (one with a name that will be duplicated multiple times)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "Multi-Duplicate", "address": "100 Pine St", "lat": 30.0, "lon": -1.0, "type": "physical"}
    ]

    # Mock scraped data with multiple items having the same base name
    mock_exists.return_value = True
    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps([
        {"name": "Multi-Duplicate", "address": "200 Pine St", "latitude": 31.0, "longitude": -2.0, "website": "", "phone": ""},
        {"name": "Multi-Duplicate", "address": "300 Pine St", "latitude": 32.0, "longitude": -3.0, "website": "", "phone": ""},
        {"name": "Multi-Duplicate", "address": "400 Pine St", "latitude": 33.0, "longitude": -4.0, "website": "", "phone": ""}
    ])

    import_stores()

    # Verify all three new stores were attempted to be added with suffixed names
    assert mock_post.call_count == 4  # One for login, three for new stores
    
    # Check the calls for adding stores
    expected_calls = [
        unittest.mock.call(STORES_URL, headers=unittest.mock.ANY, json={
            "name": "Multi-Duplicate_1",
            "type": "physical",
            "address": "200 Pine St",
            "lat": 31.0,
            "lon": -2.0,
            "homepage": ""
        }),
        unittest.mock.call(STORES_URL, headers=unittest.mock.ANY, json={
            "name": "Multi-Duplicate_2",
            "type": "physical",
            "address": "300 Pine St",
            "lat": 32.0,
            "lon": -3.0,
            "homepage": ""
        }),
        unittest.mock.call(STORES_URL, headers=unittest.mock.ANY, json={
            "name": "Multi-Duplicate_3",
            "type": "physical",
            "address": "400 Pine St",
            "lat": 33.0,
            "lon": -4.0,
            "homepage": ""
        })
    ]
    # Extract only the calls related to STORES_URL POST requests
    actual_stores_calls = [call for call in mock_post.call_args_list if call.args[0] == STORES_URL and call.kwargs.get('json')]
    
    # Compare the arguments of these calls
    for expected, actual in zip(expected_calls, actual_stores_calls):
        assert expected.args == actual.args
        assert expected.kwargs['json'] == actual.kwargs['json']



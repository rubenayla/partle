"""
This script handles the import of scraped store data (specifically ferreterias)
into the Partle backend API. It authenticates with the API, fetches existing
stores to prevent duplicates, and then uploads new store data.
"""

import requests
import json
import os
import sys

# Add the parent directory to the sys.path to allow importing app.db.models
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.db.models import StoreType

# API Configuration
BASE_URL = "http://localhost:8000"  # Adjust if your backend is running elsewhere
LOGIN_URL = f"{BASE_URL}/v1/auth/login"
STORES_URL = f"{BASE_URL}/v1/stores/"

# User Credentials (provided by you)
# TODO: These credentials should ideally be loaded from secure environment variables or a configuration management system, not hardcoded.
EMAIL = "ruben.jimenezmejias@gmail.com"
PASSWORD = "PartleRub!"

# Path to the scraped data file relative to this script
SCRAPED_DATA_FILE = "store_scrapers/ferreterias_output.json"


def get_auth_token(email, password):
    """
    Logs in to the API using the provided email and password and returns the access token.

    Args:
        email (str): The user's email for authentication.
        password (str): The user's password for authentication.

    Returns:
        str: The access token if login is successful, None otherwise.
    """
    try:
        response = requests.post(
            LOGIN_URL,
            data={"username": email, "password": password}
        )
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        print(f"Response content: {response.text if response else 'No response'}")
        return None


def get_existing_stores(token):
    """
    Fetches existing stores from the API using the provided authentication token.

    Args:
        token (str): The authentication token.

    Returns:
        list: A list of existing store dictionaries, or an empty list if an error occurs.
    """
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(STORES_URL, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching existing stores: {e}")
        print(f"Response content: {response.text if response else 'No response'}")
        return []


def import_stores():
    """
    Imports stores from the scraped data file into the backend API.
    It handles authentication, checks for exact duplicates (name, address, lat, lon),
    and suffixes store names if a name conflict exists but details are different.
    """
    token = get_auth_token(EMAIL, PASSWORD)
    if not token:
        print("Failed to get authentication token. Exiting.")
        return

    existing_stores = get_existing_stores(token)
    # Create sets for efficient duplicate checking
    existing_store_names = {store['name'] for store in existing_stores}
    existing_store_details = {
        (store.get('name'), store.get('address'), store.get('lat'), store.get('lon'))
        for store in existing_stores
    }

    # Construct the absolute path to the scraped data file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scraped_data_path = os.path.join(script_dir, SCRAPED_DATA_FILE)

    if not os.path.exists(scraped_data_path):
        print(f"Error: Scraped data file '{scraped_data_path}' not found. Please run the Scrapy spider first.")
        return

    with open(scraped_data_path, 'r', encoding='utf-8') as f:
        scraped_data = json.load(f)

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    added_count = 0
    skipped_count = 0
    name_counter = {}  # To handle name conflicts by appending numbers

    for store_data in scraped_data:
        original_name = store_data.get('name')
        current_name = original_name

        # Prepare store payload for the API
        store_payload = {
            "name": current_name,
            "type": StoreType.physical.value,  # Assuming all scraped ferreterias are physical stores
            "address": store_data.get('address'),
            "lat": store_data.get('latitude'),
            "lon": store_data.get('longitude'),
            "homepage": store_data.get('website')
        }

        # Check for exact duplicate (name, address, lat, lon)
        store_details_tuple = (
            store_payload.get('name'),
            store_payload.get('address'),
            store_payload.get('lat'),
            store_payload.get('lon')
        )
        if store_details_tuple in existing_store_details:
            print(f"Skipping exact duplicate: {original_name}")
            skipped_count += 1
            continue

        # Handle name duplicates by appending _1, _2, etc.
        # This ensures unique names for stores that might have the same name but different locations/details
        if original_name in existing_store_names or original_name in name_counter:
            if original_name not in name_counter:
                name_counter[original_name] = 0
            name_counter[original_name] += 1
            current_name = f"{original_name}_{name_counter[original_name]}"
            store_payload["name"] = current_name
            print(f"Adjusting name for potential duplicate: {original_name} -> {current_name}")

        try:
            response = requests.post(STORES_URL, headers=headers, json=store_payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print(f"Successfully added store: {current_name}")
            added_count += 1
            # Add the newly added store's details to our existing sets to prevent future duplicates in this run
            existing_store_details.add((
                store_payload.get('name'),
                store_payload.get('address'),
                store_payload.get('lat'),
                store_payload.get('lon')
            ))
            existing_store_names.add(store_payload.get('name'))  # Add the new name to the set of existing names
        except requests.exceptions.RequestException as e:
            print(f"Error adding store {current_name}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")

    print(f"Import complete. Added {added_count} stores, skipped {skipped_count} duplicates.")


if __name__ == "__main__":
    import_stores()
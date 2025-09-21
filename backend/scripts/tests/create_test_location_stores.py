#!/usr/bin/env python3
"""
Create test stores around a specific location for testing proximity algorithms.
Creates stores within 1km radius with test products and tags.
"""
import math
import random
import sys
from pathlib import Path
from typing import Tuple, List

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Store, Product, Tag, StoreType
# Schema imports not needed for direct model creation


def calculate_new_coordinates(lat: float, lon: float, distance_km: float, bearing: float) -> Tuple[float, float]:
    """
    Calculate new coordinates given a starting point, distance, and bearing.

    Args:
        lat: Starting latitude
        lon: Starting longitude
        distance_km: Distance in kilometers
        bearing: Bearing in degrees (0-360)

    Returns:
        Tuple of (new_lat, new_lon)
    """
    R = 6371  # Earth's radius in km

    # Convert to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    bearing_rad = math.radians(bearing)

    # Calculate new latitude
    new_lat_rad = math.asin(
        math.sin(lat_rad) * math.cos(distance_km / R) +
        math.cos(lat_rad) * math.sin(distance_km / R) * math.cos(bearing_rad)
    )

    # Calculate new longitude
    new_lon_rad = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(distance_km / R) * math.cos(lat_rad),
        math.cos(distance_km / R) - math.sin(lat_rad) * math.sin(new_lat_rad)
    )

    # Convert back to degrees
    new_lat = math.degrees(new_lat_rad)
    new_lon = math.degrees(new_lon_rad)

    return new_lat, new_lon


def create_test_stores(db: Session, center_lat: float, center_lon: float, num_stores: int = 10):
    """
    Create test stores around a center point.

    Args:
        db: Database session
        center_lat: Center latitude
        center_lon: Center longitude
        num_stores: Number of stores to create
    """
    print(f"\n📍 Creating {num_stores} test stores around ({center_lat}, {center_lon})")

    # Create or get the mock-data tag (general tag for all test/fake data)
    mock_tag = db.query(Tag).filter(Tag.name == "mock-data").first()
    if not mock_tag:
        mock_tag = Tag(name="mock-data")
        db.add(mock_tag)
        db.commit()
        print("✅ Created 'mock-data' tag")

    # Create or get the test-location tag (specific for location testing)
    test_tag = db.query(Tag).filter(Tag.name == "test-location").first()
    if not test_tag:
        test_tag = Tag(name="test-location")
        db.add(test_tag)
        db.commit()
        print("✅ Created 'test-location' tag")

    stores_created = []

    for i in range(num_stores):
        # Generate random distance (0.1 to 1.0 km) and bearing (0-360 degrees)
        distance = random.uniform(0.1, 1.0)
        bearing = random.uniform(0, 360)

        # Calculate new coordinates
        store_lat, store_lon = calculate_new_coordinates(center_lat, center_lon, distance, bearing)

        # Create store name and address
        store_name = f"Test Store #{i+1:02d}"
        store_address = f"Test Address {i+1}, {int(distance*1000)}m from center"

        # Check if store already exists
        existing = db.query(Store).filter(Store.name == store_name).first()
        if existing:
            print(f"⚠️  Store '{store_name}' already exists, skipping")
            continue

        # Create the store
        store = Store(
            name=store_name,
            address=store_address,
            type=StoreType.physical,
            lat=store_lat,
            lon=store_lon,
            homepage=f"https://test-store-{i+1}.example.com"
        )
        store.tags.append(mock_tag)  # Add general mock-data tag
        store.tags.append(test_tag)  # Add specific test-location tag
        db.add(store)
        db.commit()

        stores_created.append(store)
        print(f"✅ Created '{store_name}' at {distance:.2f}km, bearing {bearing:.0f}° ({store_lat:.6f}, {store_lon:.6f})")

        # Add test products to the store
        num_products = random.randint(3, 8)
        for j in range(num_products):
            product_name = f"Test Product {store.id}-{j+1}"
            product = Product(
                name=product_name,
                description=f"Test product from {store_name}",
                price=round(random.uniform(10, 200), 2),
                store_id=store.id,
                url=f"https://test-store-{i+1}.example.com/product-{j+1}"
            )
            product.tags.append(mock_tag)  # Add general mock-data tag
            product.tags.append(test_tag)  # Add specific test-location tag
            db.add(product)

        db.commit()
        print(f"   Added {num_products} test products")

    return stores_created


def test_nearest_stores(db: Session, lat: float, lon: float, max_distance_km: float = 2.0):
    """
    Test finding nearest stores to a location.

    Args:
        db: Database session
        lat: Search latitude
        lon: Search longitude
        max_distance_km: Maximum search radius in km
    """
    print(f"\n🔍 Testing nearest stores to ({lat}, {lon}) within {max_distance_km}km")

    # Get all physical stores with coordinates
    stores = db.query(Store).filter(
        Store.type == StoreType.physical,
        Store.lat.isnot(None),
        Store.lon.isnot(None)
    ).all()

    # Calculate distances
    store_distances = []
    for store in stores:
        # Haversine formula
        R = 6371  # Earth's radius in km

        lat1_rad = math.radians(lat)
        lat2_rad = math.radians(store.lat)
        delta_lat = math.radians(store.lat - lat)
        delta_lon = math.radians(store.lon - lon)

        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c

        if distance <= max_distance_km:
            store_distances.append({
                'store': store,
                'distance': distance
            })

    # Sort by distance
    store_distances.sort(key=lambda x: x['distance'])

    # Display results
    print(f"\nFound {len(store_distances)} stores within {max_distance_km}km:")
    for item in store_distances[:10]:  # Show top 10
        store = item['store']
        distance = item['distance']
        has_test_tag = any(tag.name == 'test-location' for tag in store.tags)
        tag_marker = " 🏷️" if has_test_tag else ""
        print(f"  {distance:.3f}km - {store.name}{tag_marker}")
        print(f"           📍 ({store.lat:.6f}, {store.lon:.6f})")


def cleanup_test_stores(db: Session):
    """Remove all test stores and their products."""
    print("\n🧹 Cleaning up test stores...")

    # Find mock-data tag (more general - includes all test data)
    mock_tag = db.query(Tag).filter(Tag.name == "mock-data").first()
    test_tag = db.query(Tag).filter(Tag.name == "test-location").first()

    if not mock_tag and not test_tag:
        print("No mock-data or test-location tags found")
        return

    # Find all stores with either tag
    test_stores = []
    if mock_tag:
        test_stores.extend(db.query(Store).filter(Store.tags.contains(mock_tag)).all())
    if test_tag and not mock_tag:  # Only if we don't have mock_tag to avoid duplicates
        test_stores.extend(db.query(Store).filter(Store.tags.contains(test_tag)).all())

    for store in test_stores:
        # First, find and delete products with their tags
        products = db.query(Product).filter(Product.store_id == store.id).all()
        for product in products:
            # Clear tags first
            product.tags.clear()
            db.delete(product)
        print(f"  Deleted {len(products)} products from {store.name}")

        # Clear store tags and delete store
        store.tags.clear()
        db.delete(store)

    db.commit()
    print(f"✅ Cleaned up {len(test_stores)} test stores")


def main():
    """Main function."""
    # Default center point (Madrid, Spain)
    # You can change these to your coordinates
    CENTER_LAT = 40.4168  # Madrid latitude
    CENTER_LON = -3.7038  # Madrid longitude

    print("=" * 60)
    print("TEST LOCATION STORES CREATOR")
    print("=" * 60)

    if len(sys.argv) > 1:
        if sys.argv[1] == "cleanup":
            db = SessionLocal()
            try:
                cleanup_test_stores(db)
            finally:
                db.close()
            return
        elif sys.argv[1] == "test":
            db = SessionLocal()
            try:
                test_nearest_stores(db, CENTER_LAT, CENTER_LON)
            finally:
                db.close()
            return
        elif len(sys.argv) >= 3:
            try:
                CENTER_LAT = float(sys.argv[1])
                CENTER_LON = float(sys.argv[2])
                print(f"Using custom center: ({CENTER_LAT}, {CENTER_LON})")
            except ValueError:
                print("Invalid coordinates provided")
                print_usage()
                return

    db = SessionLocal()
    try:
        # Create test stores
        stores = create_test_stores(db, CENTER_LAT, CENTER_LON, num_stores=10)

        # Test finding nearest stores
        if stores:
            test_nearest_stores(db, CENTER_LAT, CENTER_LON)
    finally:
        db.close()


def print_usage():
    """Print usage information."""
    print("\nUsage:")
    print("  python create_test_location_stores.py              # Create test stores around Madrid")
    print("  python create_test_location_stores.py <lat> <lon>  # Create test stores around custom location")
    print("  python create_test_location_stores.py test         # Test finding nearest stores")
    print("  python create_test_location_stores.py cleanup      # Remove all test stores")
    print("\nExamples:")
    print("  python create_test_location_stores.py 41.3851 2.1734  # Barcelona")
    print("  python create_test_location_stores.py 37.3891 -5.9845  # Seville")


if __name__ == "__main__":
    main()
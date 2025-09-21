#!/usr/bin/env python3
"""
Test the location-based store finding algorithm.
Verifies distance calculations and sorting work correctly.
"""
import math
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from tabulate import tabulate

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Store, StoreType


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.

    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates

    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in km

    # Convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


def test_python_algorithm(db: Session, center_lat: float, center_lon: float, radius_km: float = 1.0) -> List[Dict]:
    """
    Test the location algorithm using Python/SQLAlchemy.
    """
    print(f"\n📐 Testing Python Algorithm")
    print(f"   Center: ({center_lat:.6f}, {center_lon:.6f})")
    print(f"   Radius: {radius_km}km")

    # Query all physical stores with coordinates
    stores = db.query(Store).filter(
        Store.type == StoreType.physical,
        Store.lat.isnot(None),
        Store.lon.isnot(None)
    ).all()

    # Calculate distances
    results = []
    for store in stores:
        distance = haversine_distance(center_lat, center_lon, store.lat, store.lon)
        if distance <= radius_km:
            results.append({
                'id': store.id,
                'name': store.name,
                'distance_km': distance,
                'lat': store.lat,
                'lon': store.lon,
                'has_test_tag': any(tag.name == 'test-location' for tag in store.tags)
            })

    # Sort by distance
    results.sort(key=lambda x: x['distance_km'])
    return results


def test_sql_algorithm(db: Session, center_lat: float, center_lon: float, radius_km: float = 1.0) -> List[Dict]:
    """
    Test the location algorithm using PostgreSQL's earth_distance extension.
    """
    print(f"\n🐘 Testing PostgreSQL Algorithm")
    print(f"   Using earth_distance extension")

    # SQL query using PostgreSQL's earth_distance
    # Note: This uses the point() function and earth_distance operator
    sql = text("""
        SELECT
            s.id,
            s.name,
            s.lat,
            s.lon,
            (point(s.lon, s.lat) <@> point(:center_lon, :center_lat)) * 1.609344 AS distance_km,
            EXISTS(
                SELECT 1 FROM store_tags st
                JOIN tags t ON st.tag_id = t.id
                WHERE st.store_id = s.id AND t.name = 'test-location'
            ) AS has_test_tag
        FROM stores s
        WHERE
            s.type = 'physical'
            AND s.lat IS NOT NULL
            AND s.lon IS NOT NULL
            AND (point(s.lon, s.lat) <@> point(:center_lon, :center_lat)) * 1.609344 <= :radius_km
        ORDER BY distance_km
        LIMIT 20
    """)

    try:
        result = db.execute(sql, {
            'center_lat': center_lat,
            'center_lon': center_lon,
            'radius_km': radius_km
        })

        results = []
        for row in result:
            results.append({
                'id': row.id,
                'name': row.name,
                'distance_km': row.distance_km,
                'lat': row.lat,
                'lon': row.lon,
                'has_test_tag': row.has_test_tag
            })
        return results
    except Exception as e:
        print(f"   ⚠️  SQL algorithm failed: {e}")
        print("   Note: PostgreSQL earth_distance extension may not be installed")
        return []


def test_elasticsearch_algorithm(center_lat: float, center_lon: float, radius_km: float = 1.0) -> List[Dict]:
    """
    Test the location algorithm using Elasticsearch geo queries.
    """
    print(f"\n🔍 Testing Elasticsearch Algorithm")
    print(f"   Using geo_distance query")

    try:
        from app.search.client import search_client

        if not search_client.is_available():
            print("   ⚠️  Elasticsearch not available")
            return []

        # Elasticsearch geo query
        query = {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "geo_distance": {
                                "distance": f"{radius_km}km",
                                "location": {
                                    "lat": center_lat,
                                    "lon": center_lon
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [
                {
                    "_geo_distance": {
                        "location": {
                            "lat": center_lat,
                            "lon": center_lon
                        },
                        "order": "asc",
                        "unit": "km"
                    }
                }
            ],
            "size": 20
        }

        response = search_client.search(query)

        results = []
        for hit in response.get('hits', {}).get('hits', []):
            source = hit['_source']
            # Distance is in sort values
            distance = hit.get('sort', [0])[0] if 'sort' in hit else 0

            results.append({
                'id': source.get('id'),
                'name': source.get('store_name', source.get('name')),
                'distance_km': distance,
                'lat': source.get('location', {}).get('lat'),
                'lon': source.get('location', {}).get('lon'),
                'has_test_tag': 'test-location' in source.get('tags', [])
            })

        return results
    except Exception as e:
        print(f"   ⚠️  Elasticsearch algorithm failed: {e}")
        return []


def compare_results(results_dict: Dict[str, List[Dict]]):
    """
    Compare results from different algorithms.
    """
    print("\n" + "="*80)
    print("📊 COMPARISON OF ALGORITHMS")
    print("="*80)

    # Get all unique store IDs
    all_stores = set()
    for results in results_dict.values():
        for r in results:
            all_stores.add(r['id'])

    # Create comparison table
    comparison = []
    for store_id in sorted(all_stores):
        row = {'Store ID': store_id}

        for algo_name, results in results_dict.items():
            store_data = next((r for r in results if r['id'] == store_id), None)
            if store_data:
                row[f'{algo_name} Distance'] = f"{store_data['distance_km']:.3f}km"
                row[f'{algo_name} Rank'] = results.index(store_data) + 1
                if 'Name' not in row:
                    row['Name'] = store_data['name'][:30]  # Truncate long names
                    row['Test Store'] = '✓' if store_data['has_test_tag'] else ''
            else:
                row[f'{algo_name} Distance'] = '-'
                row[f'{algo_name} Rank'] = '-'

        comparison.append(row)

    # Sort by Python algorithm rank (our reference)
    comparison.sort(key=lambda x: x.get('Python Rank', 999))

    # Display only top 15 for readability
    print("\nTop 15 Closest Stores:")
    headers = ['Rank'] + list(comparison[0].keys()) if comparison else []
    table_data = []
    for i, row in enumerate(comparison[:15], 1):
        table_row = [i] + [row.get(h, '') for h in headers[1:]]
        table_data.append(table_row)

    print(tabulate(table_data, headers=headers, tablefmt='grid'))

    # Check for discrepancies
    print("\n🔍 Algorithm Consistency Check:")
    discrepancies = []

    for store in comparison[:10]:  # Check top 10
        distances = []
        for algo in results_dict.keys():
            dist_str = store.get(f'{algo} Distance', '-')
            if dist_str != '-':
                distances.append(float(dist_str.replace('km', '')))

        if len(distances) > 1:
            diff = max(distances) - min(distances)
            if diff > 0.01:  # More than 10 meters difference
                discrepancies.append({
                    'store': store['Name'],
                    'difference': diff
                })

    if discrepancies:
        print("   ⚠️  Distance calculation discrepancies found:")
        for d in discrepancies:
            print(f"      - {d['store']}: {d['difference']:.3f}km difference")
    else:
        print("   ✅ All algorithms agree on distances (within 10m tolerance)")


def main():
    """Main test function."""
    # Test center (Madrid)
    CENTER_LAT = 40.4168
    CENTER_LON = -3.7038
    RADIUS_KM = 1.0

    if len(sys.argv) > 1:
        try:
            CENTER_LAT = float(sys.argv[1])
            CENTER_LON = float(sys.argv[2])
            if len(sys.argv) > 3:
                RADIUS_KM = float(sys.argv[3])
        except (ValueError, IndexError):
            print("Usage: python test_location_algorithm.py [lat] [lon] [radius_km]")
            return

    print("="*80)
    print("🌍 LOCATION ALGORITHM TEST")
    print("="*80)

    db = SessionLocal()
    try:
        results = {}

        # Test Python algorithm
        python_results = test_python_algorithm(db, CENTER_LAT, CENTER_LON, RADIUS_KM)
        if python_results:
            results['Python'] = python_results
            print(f"   ✅ Found {len(python_results)} stores")

        # Test SQL algorithm
        sql_results = test_sql_algorithm(db, CENTER_LAT, CENTER_LON, RADIUS_KM)
        if sql_results:
            results['SQL'] = sql_results
            print(f"   ✅ Found {len(sql_results)} stores")

        # Test Elasticsearch algorithm
        es_results = test_elasticsearch_algorithm(CENTER_LAT, CENTER_LON, RADIUS_KM)
        if es_results:
            results['Elasticsearch'] = es_results
            print(f"   ✅ Found {len(es_results)} stores")

        # Compare results
        if len(results) > 1:
            compare_results(results)
        elif results:
            # Show results from the single algorithm that worked
            algo_name = list(results.keys())[0]
            print(f"\n📍 Results from {algo_name} Algorithm:")
            print(f"Found {len(results[algo_name])} stores within {RADIUS_KM}km:")

            for i, store in enumerate(results[algo_name][:10], 1):
                test_marker = " 🏷️" if store['has_test_tag'] else ""
                print(f"{i:2}. {store['distance_km']:.3f}km - {store['name']}{test_marker}")
                print(f"    📍 ({store['lat']:.6f}, {store['lon']:.6f})")
        else:
            print("\n❌ No algorithms were able to run")

    finally:
        db.close()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Quick test script to verify Elasticsearch search functionality.
Run this after setting up Elasticsearch to ensure everything works.
"""
import sys
import os
import requests
import json

# Add app to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.search.client import search_client
from app.search.indexing import initialize_product_index


def test_elasticsearch_connection():
    """Test basic Elasticsearch connectivity."""
    print("🔍 Testing Elasticsearch connection...")
    
    if not search_client.is_available():
        print("❌ Elasticsearch is not available")
        print("   Make sure to run: docker compose up -d elasticsearch")
        return False
    
    print("✅ Elasticsearch is available")
    
    try:
        info = search_client.client.info()
        print(f"   Cluster: {info['cluster_name']}")
        print(f"   Version: {info['version']['number']}")
    except Exception as e:
        print(f"⚠️  Could not get cluster info: {e}")
    
    return True


def test_index_exists():
    """Test that the products index exists."""
    print("\n📊 Testing search index...")
    
    try:
        exists = search_client.client.indices.exists(index=search_client.index_name)
        if exists:
            print(f"✅ Index '{search_client.index_name}' exists")
            
            # Get document count
            stats = search_client.client.indices.stats(index=search_client.index_name)
            doc_count = stats['indices'][search_client.index_name]['total']['docs']['count']
            print(f"   Documents: {doc_count}")
            
            return True
        else:
            print(f"❌ Index '{search_client.index_name}' does not exist")
            print("   Run: poetry run python manage_search.py init")
            return False
            
    except Exception as e:
        print(f"❌ Error checking index: {e}")
        return False


def test_search_query():
    """Test a basic search query."""
    print("\n🔎 Testing search query...")
    
    try:
        # Test match_all query
        response = search_client.search({
            "query": {"match_all": {}},
            "size": 5
        })
        
        total = response['hits']['total']['value']
        print(f"✅ Search works - found {total} total documents")
        
        if total > 0:
            print("   Sample results:")
            for hit in response['hits']['hits'][:3]:
                source = hit['_source']
                print(f"   - {source.get('name', 'No name')} (ID: {source.get('id')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Search query failed: {e}")
        return False


def test_api_endpoint():
    """Test the FastAPI search endpoint."""
    print("\n🌐 Testing API endpoint...")
    
    try:
        # Test if server is running
        response = requests.get("http://localhost:8000/v1/search/health", timeout=5)
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Search API is accessible")
            print(f"   Elasticsearch available: {health_data.get('elasticsearch_available')}")
            
            # Test actual search
            search_response = requests.get(
                "http://localhost:8000/v1/search/products/?q=test", 
                timeout=5
            )
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                print(f"✅ Search endpoint works - found {search_data.get('total', 0)} results")
                return True
            else:
                print(f"❌ Search endpoint failed: {search_response.status_code}")
                return False
                
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
    except requests.ConnectionError:
        print("❌ Could not connect to API server")
        print("   Make sure to run: poetry run uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def test_specific_search():
    """Test searching for 'test2' specifically (reproducing user issue)."""
    print("\n🎯 Testing specific search for 'test2'...")
    
    try:
        response = requests.get(
            "http://localhost:8000/v1/search/products/?q=test2",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            products = data.get('products', [])
            
            print(f"✅ Found {total} results for 'test2'")
            
            # Look for exact 'test2' matches
            exact_matches = [p for p in products if p.get('name') == 'test2']
            if exact_matches:
                print(f"   Found exact match: {exact_matches[0]['name']}")
                print(f"   Product ID: {exact_matches[0]['id']}")
                
                # Check if it's the first result (best relevance)
                if products and products[0].get('name') == 'test2':
                    print("✅ 'test2' is the top result (good relevance scoring)")
                else:
                    print("⚠️  'test2' is not the top result")
            else:
                print("⚠️  No exact 'test2' match found")
                if products:
                    print(f"   Top result: {products[0].get('name')}")
            
            return True
            
        else:
            print(f"❌ Search failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Specific search test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Quick Elasticsearch Search Test")
    print("=" * 50)
    
    tests = [
        test_elasticsearch_connection,
        test_index_exists,
        test_search_query,
        test_api_endpoint,
        test_specific_search
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print()
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Elasticsearch search is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
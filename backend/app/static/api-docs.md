# Partle API Documentation for ChatGPT/AI Assistants

## Quick Start

**Base URL:** https://partle.rubenayla.xyz  
**OpenAPI Spec:** https://partle.rubenayla.xyz/openapi.json  
**API Prefix:** `/v1/` (not `/api/v1/`)

## Authentication

Use the public API key in one of two ways:

### Option 1: Query Parameter (Recommended for ChatGPT)
```
?api_key=pk_test_chatgpt_readonly_key
```

### Option 2: Authorization Header
```
Authorization: Bearer pk_test_chatgpt_readonly_key
```

## Main Endpoints for ChatGPT

### 1. Search Products with Location
```
GET /v1/public/products?q=milk&lat=40.28&lon=-3.79&distance_km=5&limit=10&api_key=pk_test_chatgpt_readonly_key
```

**Parameters:**
- `q` - Search query (e.g., "milk", "bread", "electronics")
- `lat` - Latitude for location-based search
- `lon` - Longitude for location-based search  
- `distance_km` - Search radius in kilometers
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter
- `store_id` - Filter by specific store ID
- `tags` - Comma-separated tags (e.g., "organic,fresh")
- `limit` - Number of results (max 100)
- `offset` - Pagination offset

**Response Schema:**
```json
{
  "items": [
    {
      "id": 123,
      "name": "Product Name",
      "price": 9.99,
      "currency": "EUR",
      "description": "Product description",
      "url": "https://example.com/product",
      "has_image": true,
      "created_at": "2025-01-07T10:00:00Z",
      "updated_at": "2025-01-07T10:00:00Z",
      "store": {
        "id": 456,
        "name": "Store Name",
        "type": "physical",
        "address": "123 Main St, Madrid",
        "city": "Madrid",
        "country": "Spain",
        "latitude": 40.28,
        "longitude": -3.79,
        "distance_km": 1.2
      },
      "tags": ["organic", "fresh"]
    }
  ],
  "total": 100,
  "limit": 10,
  "offset": 0
}
```

### 2. Get All Stores
```
GET /v1/public/stores?lat=40.28&lon=-3.79&distance_km=10
```

**Parameters:**
- `lat` - Latitude for distance calculation
- `lon` - Longitude for distance calculation
- `distance_km` - Filter stores within radius
- `q` - Search stores by name
- `type` - Filter by type: "physical", "online", "chain"
- `limit` - Number of results
- `offset` - Pagination offset

### 3. Get Store Products
```
GET /v1/public/stores/{store_id}/products
```

Get all products from a specific store.

### 4. Get Product Details
```
GET /v1/public/products/{product_id}
```

Get detailed information about a specific product.

## Example Queries

### Find milk near a location in Madrid:
```
GET https://partle.rubenayla.xyz/v1/public/products?q=milk&lat=40.4168&lon=-3.7038&distance_km=5&api_key=pk_test_chatgpt_readonly_key
```

### Find electronics under 100 EUR:
```
GET https://partle.rubenayla.xyz/v1/public/products?q=electronics&max_price=100&api_key=pk_test_chatgpt_readonly_key
```

### Get all physical stores in Barcelona area:
```
GET https://partle.rubenayla.xyz/v1/public/stores?type=physical&lat=41.3851&lon=2.1734&distance_km=20&api_key=pk_test_chatgpt_readonly_key
```

## Rate Limits
- 100 requests per hour per API key
- Rate limit info in headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Full OpenAPI Specification
For complete API documentation with all endpoints and schemas, fetch:
```
GET https://partle.rubenayla.xyz/openapi.json
```

This returns the full OpenAPI 3.1.0 specification that can be imported into any OpenAPI-compatible tool.
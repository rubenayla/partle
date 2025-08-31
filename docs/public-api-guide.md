# Partle Public API Guide for AI Services

## Overview

The Partle Public API provides read-only access to marketplace data specifically designed for AI assistants like ChatGPT, Claude, and other automated services. This API enables AI systems to search products, browse stores, retrieve platform statistics, and provide intelligent responses about the Partle marketplace.

## Quick Start

**Base URL:** `https://partle.rubenayla.xyz`
**API Version:** v1  
**Authentication:** API Key (Bearer token)  
**Rate Limits:** 100 requests per hour per API key  

### Authentication

All API endpoints require authentication via Bearer token:

```bash
curl -H "Authorization: Bearer pk_test_chatgpt_readonly_key" \
     "https://partle.rubenayla.xyz/v1/public/products"
```

### Available API Keys

| Service | API Key | Purpose |
|---------|---------|---------|
| ChatGPT | `pk_test_chatgpt_readonly_key` | OpenAI GPT integrations |
| Claude  | `pk_test_claude_readonly_key` | Anthropic Claude integrations |

*Production keys are configured via environment variables: `CHATGPT_API_KEY` and `CLAUDE_API_KEY`*

## API Endpoints

### 1. Health Check
**No authentication required**

```http
GET /v1/public/health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-08-31T14:44:11.000Z",
  "message": "Partle API is running"
}
```

### 2. Products
Search and retrieve product information with filtering options.

```http
GET /v1/public/products
```

**Parameters:**
- `q` (string, optional): Search query for product names/descriptions
- `limit` (integer, default: 20, max: 100): Number of results to return
- `offset` (integer, default: 0): Skip items for pagination
- `min_price` (float, optional): Minimum price filter
- `max_price` (float, optional): Maximum price filter
- `tags` (string, optional): Comma-separated tag names

**Example:**
```bash
curl -H "Authorization: Bearer pk_test_chatgpt_readonly_key" \
     "https://partle.rubenayla.xyz/v1/public/products?q=electronics&limit=10&min_price=50"
```

**Response:**
```json
[
  {
    "id": 115,
    "name": "Cinta adhesiva de tejido del tipo \"americano\"",
    "spec": null,
    "url": "https://www.example.com/product/115",
    "price": 12.50,
    "image_url": "https://www.example.com/images/115.jpg",
    "store": {
      "id": 1,
      "name": "Electronics Store",
      "address": "Main St 123"
    },
    "tags": [
      {"name": "adhesive"},
      {"name": "tape"}
    ]
  }
]
```

### 3. Stores
Retrieve store information with pagination.

```http
GET /v1/public/stores
```

**Parameters:**
- `limit` (integer, default: 20, max: 50): Number of stores to return
- `offset` (integer, default: 0): Skip items for pagination

**Example:**
```bash
curl -H "Authorization: Bearer pk_test_chatgpt_readonly_key" \
     "https://partle.rubenayla.xyz/v1/public/stores?limit=5"
```

**Response:**
```json
[
  {
    "id": 2,
    "name": "Electronics Hub",
    "lat": 40.7128,
    "lon": -74.0060,
    "address": "123 Main Street, New York, NY",
    "owner_id": 10,
    "type": "physical",
    "homepage": "https://electronicshub.com"
  }
]
```

### 4. Search (Advanced)
Elasticsearch-powered product search with advanced filtering.

```http
GET /v1/public/search
```

**Parameters:**
- `q` (string, required): Search query
- `limit` (integer, default: 10, max: 50): Number of results
- `filters` (string, optional): Additional filters (implementation specific)

**Example:**
```bash
curl -H "Authorization: Bearer pk_test_chatgpt_readonly_key" \
     "https://partle.rubenayla.xyz/v1/public/search?q=smartphone&limit=5"
```

**Note:** Falls back gracefully if Elasticsearch is unavailable with error message:
```json
{
  "detail": "Search service temporarily unavailable"
}
```

### 5. Platform Statistics
Get high-level platform metrics and information.

```http
GET /v1/public/stats
```

**Example:**
```bash
curl -H "Authorization: Bearer pk_test_chatgpt_readonly_key" \
     "https://partle.rubenayla.xyz/v1/public/stats"
```

**Response:**
```json
{
  "total_products": 177,
  "total_stores": 4022,
  "last_updated": "2025-08-31T14:43:48.015305",
  "api_version": "1.0",
  "description": "Partle marketplace - Find products and stores"
}
```

## Rate Limiting

All public endpoints are rate-limited to **100 requests per hour** per client.

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 97  
X-RateLimit-Reset: 1756655052
```

**Rate Limit Exceeded:**
```json
{
  "detail": "Rate limit exceeded. Max 100 requests per 3600 seconds."
}
```

## Error Handling

### Authentication Errors

**Missing API Key:**
```http
HTTP/1.1 401 Unauthorized
{
  "detail": "Not authenticated"
}
```

**Invalid API Key:**
```http
HTTP/1.1 401 Unauthorized  
{
  "detail": "Invalid API key"
}
```

### General Errors

**Server Error:**
```http
HTTP/1.1 500 Internal Server Error
{
  "detail": "Internal server error message"
}
```

**Service Unavailable:**
```http
HTTP/1.1 503 Service Unavailable
{
  "detail": "Search service temporarily unavailable"
}
```

## AI Integration Examples

### ChatGPT Custom GPT Configuration

For ChatGPT Custom GPT creation:

1. **Authentication:** API Key
2. **API Key:** `pk_test_chatgpt_readonly_key`
3. **Schema:** Import from `https://partle.rubenayla.xyz/openapi.json`
4. **Base URL:** `https://partle.rubenayla.xyz`

### Claude MCP Integration

Claude can access the API through the MCP manifest file:

```bash
# Point Claude to your MCP manifest
/path/to/partle/mcp-manifest.json
```

### Direct API Integration

For custom AI applications:

```python
import httpx

class PartleAPI:
    def __init__(self, api_key: str, base_url: str = "https://partle.rubenayla.xyz"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def search_products(self, query: str, limit: int = 20):
        response = httpx.get(
            f"{self.base_url}/v1/public/products",
            headers=self.headers,
            params={"q": query, "limit": limit}
        )
        return response.json()
    
    def get_stats(self):
        response = httpx.get(
            f"{self.base_url}/v1/public/stats",
            headers=self.headers
        )
        return response.json()

# Usage
api = PartleAPI("pk_test_chatgpt_readonly_key")
products = api.search_products("electronics", limit=10)
stats = api.get_stats()
```

## Use Case Examples

### E-commerce Assistant
```
User: "Find me wireless headphones under €100"
AI Query: GET /v1/public/products?q=wireless headphones&max_price=100
AI Response: Lists matching wireless headphone products with prices, store info, and links
```

### Business Intelligence
```  
User: "How many stores are in the platform?"
AI Query: GET /v1/public/stats
AI Response: "The Partle marketplace currently has 4,022 stores and 177 products."
```

### Store Locator
```
User: "Show me electronics stores"
AI Query: GET /v1/public/stores + filter analysis
AI Response: Lists stores with electronics products, including addresses and contact info
```

### Product Comparison
```
User: "Compare prices for smartphones"
AI Query: Multiple calls to /v1/public/products?q=smartphone
AI Response: Comparative analysis of smartphone prices across different stores
```

## Best Practices for AI Integration

### 1. Efficient Query Patterns
- **Use specific search terms** rather than broad queries
- **Implement pagination** for large result sets
- **Combine filters** to narrow results effectively

### 2. Error Handling
- **Respect rate limits** and implement backoff strategies
- **Handle service unavailability** gracefully (especially search)
- **Validate API responses** before processing

### 3. Caching Strategy
- **Cache platform stats** (low update frequency)
- **Cache store information** (relatively static)
- **Don't cache product searches** (dynamic results)

### 4. User Experience
- **Provide source attribution** ("According to Partle marketplace...")
- **Include direct links** to products when available
- **Format prices with currency** (€ symbol)

## API Limits and Quotas

| Endpoint | Rate Limit | Max Results | Notes |
|----------|------------|-------------|-------|
| `/health` | Unlimited | - | No auth required |
| `/products` | 100/hour | 100 per request | Most used endpoint |
| `/stores` | 100/hour | 50 per request | Less frequently updated |
| `/search` | 100/hour | 50 per request | Requires Elasticsearch |
| `/stats` | 100/hour | - | Recommended caching |

## Development vs Production

### Production Environment  
- **Base URL:** `https://partle.rubenayla.xyz`
- **API Keys:** Production keys (via environment variables)
- **CORS:** Restricted origins  
- **Rate Limits:** Strictly enforced
- **HTTPS:** Required for all requests

## Troubleshooting

### Common Issues

**1. 401 Authentication Error**
- Verify API key is correct
- Check Bearer token format
- Ensure key hasn't expired

**2. Rate Limit Exceeded**
- Implement exponential backoff
- Reduce request frequency
- Consider request batching

**3. Search Service Unavailable**  
- Fall back to `/products` endpoint
- Implement retry logic
- User-friendly error messages

**4. Slow Response Times**
- Check network connectivity
- Reduce result limits
- Use more specific queries

### Getting Help

- **API Documentation:** `https://partle.rubenayla.xyz/docs`
- **OpenAPI Schema:** `https://partle.rubenayla.xyz/openapi.json` 
- **MCP Integration:** `docs/chatgpt-integration.md`
- **Issues:** GitHub repository issues section

## Changelog

### Version 1.0.0 (2025-08-31)
- Initial public API release
- Authentication with API keys
- Rate limiting implementation
- Full CRUD operations for products and stores
- Platform statistics endpoint
- Elasticsearch integration with fallback
- Comprehensive error handling
- CORS support for web applications

---

The Partle Public API is designed specifically for AI assistant integration, providing reliable access to marketplace data while maintaining security and performance standards. Start with the basic endpoints and gradually explore advanced features as your integration needs grow.
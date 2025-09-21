# ChatGPT Integration with Partle MCP Servers

## Overview

This guide explains how to connect ChatGPT to your Partle MCP servers, enabling ChatGPT to access your Partle platform data and perform sophisticated analysis through natural language queries.

## Prerequisites

1. **Running Partle Backend**: Your FastAPI server must be running on `http://localhost:8000`
2. **MCP Servers**: At least one Partle MCP server should be available
3. **ChatGPT Plus/Pro Account**: Required for MCP integrations
4. **Local Development Environment**: MCP servers run locally

## Auto-Discovery Process

ChatGPT can automatically discover and connect to your Partle MCP servers using several methods:

### Method 1: MCP Manifest Auto-Discovery

1. **Place the Manifest File**: 
   ```bash
   # Your mcp-manifest.json should be in your project root
   /path/to/partle/mcp-manifest.json
   ```

2. **ChatGPT Discovery**:
   - ChatGPT will scan common locations for MCP manifests
   - It looks for `mcp-manifest.json` in project roots
   - The manifest describes all available Partle servers

3. **Automatic Configuration**:
   - ChatGPT reads server capabilities from the manifest
   - Configures connection parameters automatically
   - Sets up proper environment variables

### Method 2: Documentation-Based Discovery

ChatGPT can discover your servers by reading the setup documentation:

1. **Documentation Files**:
   ```
   docs/mcp-setup.md          # Main setup guide
   docs/chatgpt-integration.md # This file
   mcp-manifest.json          # Server manifest
   ```

2. **Discovery Process**:
   - ChatGPT scans for MCP-related documentation
   - Extracts server commands and capabilities
   - Builds configuration from available information

### Method 3: Direct API Discovery

If your Partle API includes MCP endpoint information:

1. **API Endpoint**: `GET /v1/mcp/servers`
2. **Response Format**:
   ```json
   {
     "servers": [
       {
         "name": "partle-products",
         "description": "Product search and analysis",
         "command": ["python", "backend/scripts/run_mcp_products.py"],
         "capabilities": ["search_products", "get_product"],
         "status": "available"
       }
     ]
   }
   ```

## Manual Configuration Guide

If auto-discovery doesn't work, configure ChatGPT manually:

### Step 1: Start MCP Servers

```bash
# Start the servers you need
cd /path/to/partle

# Products server (most commonly used)
uv run python backend/scripts/run_mcp_products.py &

# Analytics server (for business intelligence)
uv run python backend/scripts/run_mcp_analytics.py &

# Add others as needed
uv run python backend/scripts/run_mcp_stores.py &
```

### Step 2: Configure ChatGPT

1. **Open ChatGPT Settings**:
   - Go to Settings → Beta Features → Model Context Protocol

2. **Add MCP Server**:
   - **Name**: `Partle Products`
   - **Description**: `Access to Partle product database and search`
   - **Command**: `python backend/scripts/run_mcp_products.py`
   - **Working Directory**: `/path/to/partle`
   - **Environment Variables**:
     ```
     PARTLE_API_URL=http://localhost:8000
     ```

3. **Repeat for Other Servers**:
   ```
   Server: Partle Analytics
   Command: python backend/scripts/run_mcp_analytics.py
   
   Server: Partle Stores  
   Command: python backend/scripts/run_mcp_stores.py
   
   Server: Partle Price Intelligence
   Command: python backend/scripts/run_mcp_price_intelligence.py
   ```

### Step 3: Test Configuration

Try these test queries in ChatGPT:

```
"Search for products in the Partle database"
"Show me platform analytics overview"  
"Find stores near a specific location"
"Analyze pricing trends in electronics"
```

## Usage Examples

### Basic Product Queries
```
User: "What products do we have in electronics category?"
ChatGPT: Uses partle-products server → search_products tool with tags filter

User: "Show me the most expensive items"
ChatGPT: Uses partle-products server → search_products with sort_by="price_desc"
```

### Business Intelligence Queries  
```
User: "Give me a platform overview with key metrics"
ChatGPT: Uses partle-analytics server → get_platform_overview tool

User: "Which stores are performing best?"
ChatGPT: Uses partle-analytics server → get_top_performers tool
```

### Location-Based Analysis
```
User: "Find stores within 10km of coordinates 40.7128, -74.0060"
ChatGPT: Uses partle-stores server → find_stores_near_location tool

User: "Identify market gaps for expansion"  
ChatGPT: Uses partle-location-intelligence server → find_market_gaps tool
```

### Advanced Analysis
```
User: "Compare pricing strategies across our top 5 stores"
ChatGPT: Uses partle-price-intelligence server → compare_store_pricing tool

User: "Recommend products similar to product ID 123"
ChatGPT: Uses partle-recommendations server → recommend_similar_products tool
```

## Server Selection Guide

ChatGPT will automatically choose the right server based on your query:

| Query Type | Primary Server | Fallback Servers |
|------------|----------------|------------------|
| Product search | Products | Analytics, Recommendations |
| Store information | Stores | Analytics, Location Intelligence |
| Business metrics | Analytics | Products, Stores |
| Pricing analysis | Price Intelligence | Analytics, Products |
| Location queries | Location Intelligence | Stores |
| Recommendations | Recommendations | Products, Analytics |

## Troubleshooting

### Connection Issues

1. **Server Not Found**:
   ```bash
   # Check if server process is running
   ps aux | grep mcp
   
   # Restart server manually
   uv run python backend/scripts/run_mcp_products.py
   ```

2. **API Connection Failed**:
   ```bash
   # Test API connectivity
   curl http://localhost:8000/v1/products/
   
   # Check environment variables
   echo $PARTLE_API_URL
   ```

3. **ChatGPT Can't Connect**:
   - Verify working directory path is correct
   - Check that Python and UV are in PATH
   - Ensure no firewall blocking connections

### Discovery Issues

1. **Manifest Not Found**:
   ```bash
   # Verify manifest location
   ls -la mcp-manifest.json
   
   # Check file permissions
   chmod 644 mcp-manifest.json
   ```

2. **Servers Not Auto-Detected**:
   - Check that server scripts are executable
   - Verify manifest syntax is valid JSON
   - Ensure documentation files are present

### Performance Issues

1. **Slow Responses**:
   - Check Partle API performance
   - Reduce query complexity
   - Use specific rather than broad queries

2. **Memory Usage**:
   - Don't run all servers simultaneously unless needed
   - Monitor system resources
   - Restart servers periodically

## Security Considerations

### Local Development
- MCP servers run locally only
- No external network access required
- Data stays on your machine

### Production Considerations
- Use proper authentication on Partle API
- Consider VPN for remote access
- Monitor server logs for unusual activity
- Use environment-specific configurations

## Advanced Configuration

### Custom Environment Setup

Create a `.env.mcp` file:
```bash
PARTLE_API_URL=http://localhost:8000
MCP_LOG_LEVEL=INFO
MCP_TIMEOUT=120
MCP_MAX_CONNECTIONS=10
```

### Server-Specific Settings

Each server can be customized:

```json
{
  "partle-products": {
    "max_results": 100,
    "enable_elasticsearch": true,
    "cache_timeout": 300
  },
  "partle-analytics": {
    "enable_advanced_metrics": true,
    "calculation_timeout": 60
  }
}
```

## API Integration Examples

### Custom MCP Discovery Endpoint

Add to your Partle FastAPI app:

```python
@app.get("/v1/mcp/servers")
def get_mcp_servers():
    return {
        "servers": [
            {
                "name": "partle-products",
                "description": "Product search and management",
                "command": ["python", "backend/scripts/run_mcp_products.py"],
                "capabilities": ["search_products", "get_product"],
                "status": "available",
                "health_check": "/v1/products/",
                "documentation": "/docs/mcp-api.md#products"
            }
        ],
        "manifest_url": "/mcp-manifest.json",
        "documentation": "/docs/mcp-setup.md"
    }
```

### Health Check Endpoint

```python
@app.get("/v1/mcp/health")
def mcp_health():
    return {
        "status": "healthy",
        "servers_available": 6,
        "api_version": "1.0.0",
        "last_updated": "2025-08-31T00:00:00Z"
    }
```

## Best Practices

1. **Start with Core Servers**: Begin with Products and Analytics servers
2. **Use Specific Queries**: More targeted requests get better results  
3. **Monitor Performance**: Watch API response times and server resource usage
4. **Regular Updates**: Keep MCP library and servers updated
5. **Documentation**: Keep server capabilities documentation current

## Next Steps

1. **Test Basic Functionality**: Try simple product searches first
2. **Explore Advanced Features**: Experiment with analytics and intelligence servers
3. **Custom Integration**: Modify servers for your specific business needs
4. **Production Deployment**: Consider deployment strategies for production use

The MCP integration provides powerful natural language access to your Partle data - start simple and gradually explore more advanced capabilities as you become comfortable with the system.
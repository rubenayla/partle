# Partle MCP Servers Setup Guide

## Overview

The Partle Model Context Protocol (MCP) servers provide ChatGPT and other AI assistants with direct access to your Partle platform data and functionality. These servers enable sophisticated analysis, recommendations, and insights through natural language interactions.

## Available MCP Servers

### 1. **Products Server** (`partle-products`)
- Search and filter products across the platform
- Advanced Elasticsearch-powered search capabilities
- Product details and store associations
- **Use Cases**: Product discovery, inventory analysis, competitive research

### 2. **Stores Server** (`partle-stores`)  
- Store discovery and location-based queries
- Store analytics and performance metrics
- Geographic and demographic analysis
- **Use Cases**: Store management, market expansion, location analysis

### 3. **Analytics Server** (`partle-analytics`)
- Platform-wide business intelligence
- Performance metrics and KPI tracking
- Market insights and trend analysis
- **Use Cases**: Business reporting, strategic planning, market research

### 4. **Price Intelligence Server** (`partle-price-intelligence`)
- Competitive pricing analysis
- Price trend identification and forecasting
- Market positioning insights
- **Use Cases**: Pricing strategy, competitive analysis, profit optimization

### 5. **Location Intelligence Server** (`partle-location-intelligence`)
- Geographic market analysis
- Store density and coverage mapping
- Optimal location recommendations
- **Use Cases**: Expansion planning, market penetration, location strategy

### 6. **Recommendations Server** (`partle-recommendations`)
- Personalized product recommendations
- Trend detection and popularity analysis
- Shopping list optimization
- **Use Cases**: Customer experience, sales optimization, product discovery

## Prerequisites

### System Requirements
- Python 3.12 or higher
- UV package manager
- Running Partle backend server
- MCP-compatible AI client (ChatGPT, Claude, etc.)

### Installation

1. **Install Dependencies**
   ```bash
   cd backend/
   uv sync
   ```

2. **Verify Installation**
   ```bash
   uv run python -c "from mcp.server import Server; print('MCP installed successfully')"
   ```

3. **Start Partle Backend**
   ```bash
   # Make sure your Partle API is running
   uv run uvicorn app.main:app --reload
   ```

## Quick Start

### Running Individual Servers

Each MCP server can be started independently:

```bash
# Products server
uv run python backend/scripts/run_mcp_products.py

# Stores server  
uv run python backend/scripts/run_mcp_stores.py

# Analytics server
uv run python backend/scripts/run_mcp_analytics.py

# Price intelligence server
uv run python backend/scripts/run_mcp_price_intelligence.py

# Location intelligence server
uv run python backend/scripts/run_mcp_location_intelligence.py

# Recommendations server
uv run python backend/scripts/run_mcp_recommendations.py
```

### Testing Server Connection

Test that servers are working correctly:

```bash
# Test products server import
uv run python -c "from app.mcp.products import mcp_server; print('Products server ready')"

# Test with a simple query (if your API has data)
uv run python backend/scripts/run_mcp_products.py &
# Server will start and listen for MCP connections
```

## Configuration

### Environment Variables

Set these environment variables for optimal performance:

```bash
# Required
export PARTLE_API_URL="http://localhost:8000"

# Optional
export MCP_LOG_LEVEL="INFO"
export MCP_TIMEOUT="120"
```

### API Configuration

Ensure your Partle API is configured with:

- **Products API** (`/v1/products/`)
- **Stores API** (`/v1/stores/`)  
- **Search API** (`/v1/search/products/`) - for Elasticsearch features
- **Proper CORS settings** for MCP connections

## Connecting to ChatGPT

### Step 1: Start MCP Servers

Choose which servers you need and start them:

```bash
# Example: Start products and analytics servers
uv run python backend/scripts/run_mcp_products.py &
uv run python backend/scripts/run_mcp_analytics.py &
```

### Step 2: Configure ChatGPT

1. **Open ChatGPT Settings**
2. **Navigate to MCP/External Tools**
3. **Add New MCP Server**:
   - **Name**: `Partle Products`
   - **Command**: `python backend/scripts/run_mcp_products.py`
   - **Working Directory**: `/path/to/partle`
   - **Environment Variables**: `PARTLE_API_URL=http://localhost:8000`

### Step 3: Test Connection

In ChatGPT, try commands like:
- "Show me the latest products in the Partle database"
- "Analyze store performance metrics"
- "Find pricing outliers in electronics category"
- "Recommend optimal locations for new stores"

## Server Capabilities Overview

| Server | Key Functions | Best For |
|--------|---------------|----------|
| **Products** | Search, filter, product details | Product discovery, catalog management |
| **Stores** | Location search, store analytics | Store operations, location analysis |
| **Analytics** | Platform metrics, business intelligence | Strategic planning, reporting |
| **Price Intelligence** | Pricing analysis, competitive insights | Pricing strategy, market positioning |
| **Location Intelligence** | Geographic analysis, market gaps | Expansion planning, location strategy |
| **Recommendations** | Product suggestions, trend analysis | Customer experience, sales optimization |

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   # Make sure you're in the backend directory and using uv
   cd backend/
   uv sync
   uv run python scripts/run_mcp_products.py
   ```

2. **API connection failures**
   ```bash
   # Verify your Partle API is running
   curl http://localhost:8000/v1/products/
   
   # Check environment variables
   echo $PARTLE_API_URL
   ```

3. **Server startup issues**
   ```bash
   # Check for port conflicts
   lsof -i :8000
   
   # Restart with verbose logging
   MCP_LOG_LEVEL=DEBUG uv run python scripts/run_mcp_products.py
   ```

### Performance Tips

1. **Start only needed servers** - Each server uses resources
2. **Use specific queries** - More targeted requests get better responses
3. **Monitor API performance** - Ensure your Partle backend is responsive
4. **Batch operations** - Multiple related queries work efficiently

## Security Considerations

- **Local Network Only**: MCP servers should only be accessible locally
- **API Authentication**: Ensure proper authentication on your Partle API
- **Data Privacy**: MCP servers access your business data directly
- **Network Security**: Use appropriate firewall rules for production

## Next Steps

1. **Read the API Reference**: `docs/mcp-api.md`
2. **Try the Examples**: `docs/mcp-examples.md`
3. **Customize for Your Needs**: Modify server configurations as needed
4. **Integration**: Connect with your preferred AI assistant

## Support

For issues with MCP servers:
1. Check the logs for error messages
2. Verify your Partle API is working correctly  
3. Ensure proper environment configuration
4. Test individual server components

The MCP servers provide powerful integration capabilities - start with one server and gradually add others based on your needs.
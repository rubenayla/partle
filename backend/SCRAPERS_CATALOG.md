# Partle Scrapers Catalog

## Overview
The Partle platform includes a comprehensive scraping system with 14 different web scrapers targeting various e-commerce and retail websites. These scrapers collect product information including names, prices, descriptions, images, and tags.

## Scraper Management
All scrapers can be managed through the MCP Scraper Monitor interface, which provides:
- Start/stop individual scrapers
- Bulk operations for multiple scrapers
- Real-time status monitoring
- Log viewing and debugging
- Database statistics

## Available Scrapers

### 🔨 Hardware/DIY Category

#### 1. **Brico Depot** (`bricodepot`)
- **URL**: https://www.bricodepot.es
- **Description**: Spanish DIY and construction materials retailer
- **Products**: Building materials, tools, garden supplies, home improvement
- **Coverage**: Spain
- **Update Frequency**: Daily recommended

#### 2. **Brico Depot Simple** (`bricodepot_simple`)
- **URL**: https://www.bricodepot.es
- **Description**: Simplified version for specific categories
- **Products**: Focused subset of Brico Depot catalog
- **Coverage**: Spain
- **Use Case**: Faster updates for high-priority categories

#### 3. **Leroy Merlin** (`leroy_merlin`)
- **URL**: https://www.leroymerlin.es
- **Description**: Major European home improvement and gardening retailer
- **Products**: Home improvement, gardening, decoration, tools
- **Coverage**: Spain, Europe-wide chain
- **Update Frequency**: Daily recommended

#### 4. **Bauhaus** (`bauhaus`)
- **URL**: https://www.bauhaus.es
- **Description**: German DIY and building materials chain
- **Products**: Professional tools, building supplies, workshop equipment
- **Coverage**: Spain, Germany-based chain
- **Update Frequency**: Weekly

### 🔧 Hardware Stores

#### 5. **Ferreterías** (`ferreterias`)
- **URL**: Various local stores
- **Description**: Aggregates multiple Spanish hardware stores
- **Products**: Traditional hardware, fasteners, hand tools
- **Coverage**: Local Spanish ferreterías
- **Update Frequency**: Weekly

#### 6. **Ferreteria Shop** (`ferreteria_shop`)
- **URL**: https://www.ferreteria.shop
- **Description**: Online hardware store
- **Products**: Hardware supplies, tools, industrial products
- **Coverage**: Online, Spain-focused
- **Update Frequency**: Daily

### 🏭 Industrial/Professional

#### 7. **Mengual** (`mengual`)
- **URL**: https://www.mengual.es
- **Description**: Industrial supplies and professional tools
- **Products**: Industrial equipment, professional tools, safety equipment
- **Coverage**: B2B focused, Spain
- **Update Frequency**: Weekly

#### 8. **Mengual Simple** (`mengual_simple`)
- **URL**: https://www.mengual.es
- **Description**: Simplified scraper for specific categories
- **Products**: Subset of Mengual catalog
- **Use Case**: Quick updates for popular items

#### 9. **Mengual Bulk** (`mengual_bulk`)
- **URL**: https://www.mengual.es
- **Description**: Bulk product scraper for large catalogs
- **Products**: Bulk industrial supplies
- **Use Case**: Comprehensive catalog scraping

### 🛒 General Retail

#### 10. **Carrefour** (`carrefour`)
- **URL**: https://www.carrefour.es
- **Description**: French multinational retail corporation
- **Products**: Supermarket items, electronics, home goods
- **Coverage**: Spain, international chain
- **Update Frequency**: Daily for key categories

### 💻 Electronics/Technology

#### 11. **Rational Stock** (`rationalstock`)
- **URL**: https://www.rationalstock.es
- **Description**: Electronics and technology products
- **Products**: Computer parts, electronics, tech accessories
- **Coverage**: Spain, online
- **Update Frequency**: Daily

#### 12. **Rational Stock Simple** (`rationalstock_simple`)
- **URL**: https://www.rationalstock.es
- **Description**: Simplified version for popular categories
- **Products**: High-demand tech products
- **Use Case**: Frequent price monitoring

### 📦 Direct Sales

#### 13. **Products Direct** (`products_direct`)
- **URL**: https://www.products-direct.es
- **Description**: Direct import and sales platform
- **Products**: Various imported goods, wholesale items
- **Coverage**: Spain, import focus
- **Update Frequency**: Weekly

## Usage Examples

### Starting a Single Scraper
```bash
# Start Brico Depot scraper
cd backend/app/scraper
uv run python run_spider.py bricodepot

# With debug logging
uv run python run_spider.py bricodepot --log-level=DEBUG

# Fresh start (no resume)
uv run python run_spider.py bricodepot --no-resume
```

### Using MCP Scraper Monitor

Through the MCP interface, you can:

1. **List all scrapers**: Shows status, categories, and URLs
2. **Start scraper**: `start_scraper(spider_name="bricodepot")`
3. **Bulk operations**: `bulk_start_scrapers(spider_names=["bricodepot", "leroy_merlin"])`
4. **View logs**: `get_scraper_status(spider_name="bricodepot", log_lines=100)`
5. **Get statistics**: `get_scraper_stats()` shows product counts by store

## Scheduling Recommendations

### Daily Updates
- `bricodepot` - High turnover DIY products
- `leroy_merlin` - Popular home improvement
- `ferreteria_shop` - Online-only with frequent changes
- `rationalstock` - Tech products with volatile pricing
- `carrefour` - Supermarket items (selected categories)

### Weekly Updates
- `bauhaus` - Professional tools, stable prices
- `ferreterias` - Traditional hardware stores
- `mengual` - Industrial B2B products
- `products_direct` - Import/wholesale items

### On-Demand
- `*_simple` variants - For quick targeted updates
- `mengual_bulk` - For comprehensive catalog refreshes

## Database Storage

All scraped products are stored with:
- Product name and description
- Current price and currency
- Store association
- Images (stored as binary in database)
- Tags for categorization
- SKU for unique identification
- Timestamps for tracking updates

## Configuration

Each scraper requires:
1. **Store ID**: Must exist in database `stores` table
2. **User ID**: For attribution (set in `SCRAPER_USER_ID`)
3. **Database URL**: PostgreSQL connection string

Environment variables in `backend/.env`:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/partle
SCRAPER_USER_ID=1
BRICODEPOT_STORE_ID=1
LEROY_MERLIN_STORE_ID=2
# ... etc for each scraper
```

## Error Handling

The scraping system includes:
- Automatic retries for failed requests
- Resume capability for interrupted scrapes
- Duplicate detection to avoid redundant entries
- Comprehensive logging for debugging
- Rate limiting to respect website policies

## Best Practices

1. **Respect robots.txt**: All scrapers should follow website policies
2. **Rate limiting**: Avoid overwhelming target servers
3. **Schedule wisely**: Run during off-peak hours when possible
4. **Monitor logs**: Check for errors and blocked requests
5. **Update selectors**: Websites change; maintain scraper accuracy
6. **Test first**: Use `--dry-run` before production runs

## Monitoring

Check scraper health with:
- Log files in `backend/app/scraper/logs/`
- Database product counts per store
- MCP monitor for real-time status
- Error rates and success metrics

## Future Additions

Potential new scrapers for:
- Amazon.es - Major e-commerce platform
- AliExpress - International marketplace
- MediaMarkt - Electronics retailer
- El Corte Inglés - Department store
- Local specialized stores
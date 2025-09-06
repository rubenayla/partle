# Backend Scripts Organization

## Directory Structure

### `/scripts/tests/`
Test scripts for various functionality:
- `test_email_debug.py` - Email functionality testing
- `test_mcp_scraper.py` - MCP scraper testing
- `test_search_quick.py` - Quick search verification
- `test_your_email.py` - Email configuration testing
- `add_test_images.py` - Add test images to products
- `create_test_stores.py` - Create test store data

### `/scripts/utils/`
Utility scripts for maintenance and management:
- `manage_search.py` - Elasticsearch index management
- `tag_stores_products.py` - Tag stores as online/in-store
- `remove_example_products.py` - Clean up example data

### `/scripts/migrations/`
Data migration and transformation scripts:
- `migrate_local_to_remote.py` - Migrate data between databases
- `merge_bricodepot_stores.py` - Merge duplicate Brico Depot stores

### `/scripts/scrapers/`
Scraper monitoring and management:
- `check_scrapers_status.py` - Monitor scraper status
- `check_mengual_store.py` - Check specific store scraping
- `mcp_scraper_monitor.py` - MCP scraper monitoring

### `/scripts/debug_email/`
Email system debugging (existing):
- `debug_email_direct.py`
- `debug_password_reset.py`
- `debug_password_reset_auto.py`

## Running Scripts

All scripts should be run from the `/backend` directory using Poetry:

```bash
# Examples:
poetry run python scripts/tests/test_search_quick.py
poetry run python scripts/utils/manage_search.py setup
poetry run python scripts/utils/tag_stores_products.py
```

## Root Directory Files

Only essential configuration files remain in the backend root:
- `conftest.py` - pytest configuration (required in root)
- `generate_openapi.py` - OpenAPI schema generation utility
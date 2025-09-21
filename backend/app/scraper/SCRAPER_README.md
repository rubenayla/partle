# Partle Scraper

A reliable, resumable web scraper for e-commerce product data using Scrapy.

## Features

- **Database Integration**: Direct database storage via SQLAlchemy pipelines
- **Duplicate Detection**: Smart duplicate filtering and product updates
- **Resumable Crawls**: Built-in support for pausing and resuming crawls
- **Cron-Friendly**: Designed for scheduled execution with proper logging
- **Error Handling**: Robust error recovery and detailed logging
- **Configuration Management**: Environment-based configuration

## Quick Start

1. **Set up environment variables:**
   ```bash
   cp ../../../../.env.example ../../../../.env
   # Edit .env with your database credentials and settings
   ```

2. **Run a spider manually:**
   ```bash
   # From the scraper directory
   uv run python run_spider.py bricodepot
   ```

3. **Run with custom options:**
   ```bash
   # Debug mode with custom log file
   uv run python run_spider.py bricodepot --log-level=DEBUG --log-file=custom.log
   
   # Fresh start (no resume)
   uv run python run_spider.py bricodepot --no-resume
   
   # Dry run (no database changes)
   uv run python run_spider.py bricodepot --dry-run
   ```

## Cron Setup

To run scrapers automatically, add to your crontab:

```bash
# Run bricodepot scraper daily at 2 AM
0 2 * * * cd /path/to/partle/backend/app/scraper && /path/to/uv run python run_spider.py bricodepot >> /var/log/scraper.log 2>&1

# Run multiple spiders at different times
0 2 * * * cd /path/to/partle/backend/app/scraper && /path/to/uv run python run_spider.py bricodepot
0 4 * * * cd /path/to/partle/backend/app/scraper && /path/to/uv run python run_spider.py leroy_merlin
0 6 * * * cd /path/to/partle/backend/app/scraper && /path/to/uv run python run_spider.py ferreterias
```

## Available Spiders

- `bricodepot` - Scrapes products from Brico Depot
- `leroy_merlin` - Scrapes products from Leroy Merlin  
- `ferreterias` - Scrapes products from local hardware stores

## Configuration

Environment variables (set in `.env` file):

- `DATABASE_URL` - PostgreSQL connection string
- `BRICODEPOT_STORE_ID` - Store ID for Brico Depot in your database
- `LEROY_MERLIN_STORE_ID` - Store ID for Leroy Merlin in your database
- `FERRETERIAS_STORE_ID` - Store ID for ferreterias in your database
- `SCRAPER_USER_ID` - User ID to attribute scraped products to
- `ENABLE_DUPLICATE_FILTER` - Enable duplicate detection (true/false)
- `UPDATE_EXISTING_PRODUCTS` - Update existing products (true/false)
- `SCRAPER_LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)

## Database Schema

The scraper works with these main tables:
- `stores` - Store information
- `products` - Product data with timestamps and user tracking
- `users` - User accounts (for attribution)

## Monitoring

Logs are automatically created in the `logs/` directory with timestamps. Each run includes:
- Detailed processing information
- Error tracking with stack traces
- Statistics (items processed, created, updated, duplicates)
- Performance metrics

## Troubleshooting

1. **Database connection errors**: Check `DATABASE_URL` in `.env`
2. **Missing store IDs**: Ensure stores exist in database with correct IDs
3. **Permission errors**: Check file permissions on log directory
4. **Spider not found**: Verify spider name matches file in `spiders/` directory

## Development

To add a new spider:

1. Create spider file in `store_scrapers/spiders/`
2. Use `ProductItem` for scraped data
3. Add store ID to `config.py`
4. Test with `--dry-run` option first
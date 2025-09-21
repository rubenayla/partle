# Scraper Module

This module is responsible for scraping product and store data from various online sources and importing it into the Partle backend. It leverages Scrapy for web crawling and a custom Python script for data ingestion.

## Architecture

- **Scrapy Spiders (`store_scrapers/spiders/`):** Contains individual spiders (e.g., `bricodepot.py`, `ferreterias.py`, `leroy_merlin.py`) designed to crawl specific websites and extract relevant data.
- **Scrapy Project (`store_scrapers/`):** Configures the Scrapy spiders, pipelines, and middlewares.
- **Data Import Script (`import_ferreterias.py`):** A standalone script that reads scraped data (typically JSON output from Scrapy) and imports it into the Partle backend API.

## How to Run Spiders

To run a specific Scrapy spider, navigate to the `backend/app/scraper/` directory and use the `uv run scrapy crawl` command:

```bash
cd backend/app/scraper/
uv run scrapy crawl <spider_name>
```

Replace `<spider_name>` with the name of the spider you want to run (e.g., `bricodepot`, `ferreterias`, `leroy_merlin`).

## Data Import

After a spider has successfully scraped data (usually output to a JSON file like `store_scrapers/ferreterias_output.json` or `store_scrapers/output_bricodepot.json`), you can import it into the backend database using the `import_ferreterias.py` script:

```bash
cd backend/app/scraper/
uv run python import_ferreterias.py
```

This script handles authentication with the backend and manages duplicate entries based on store name, address, latitude, and longitude.

## Key Files

- `store_scrapers/spiders/`: Directory containing the Scrapy spider definitions.
- `store_scrapers/settings.py`: Scrapy project settings (e.g., user agents, concurrency, Playwright configuration).
- `import_ferreterias.py`: Script for importing scraped data into the backend.
- `store_scrapers/items.py`: Defines the data structure for scraped items.

## Further Documentation

For detailed information on individual spiders, refer to their respective docstrings and comments within the spider files.

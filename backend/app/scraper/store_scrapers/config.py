"""
Configuration management for the scraper.
"""
import os
from typing import Optional


class ScraperConfig:
    """Configuration class for scraper settings."""
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://user:password@localhost/partle"
    )
    
    # API settings (fallback for testing)
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    # Default user ID for scraped products (system user)
    DEFAULT_CREATOR_ID: Optional[int] = int(os.getenv("SCRAPER_USER_ID", "1")) if os.getenv("SCRAPER_USER_ID") else None
    
    # Store IDs mapping
    STORE_IDS = {
        "bricodepot": int(os.getenv("BRICODEPOT_STORE_ID", "4064")),
        "leroy_merlin": int(os.getenv("LEROY_MERLIN_STORE_ID", "4065")),
        "ferreterias": int(os.getenv("FERRETERIAS_STORE_ID", "4066")),
    }
    
    # Scraping behavior
    ENABLE_DUPLICATE_FILTER: bool = os.getenv("ENABLE_DUPLICATE_FILTER", "true").lower() == "true"
    UPDATE_EXISTING_PRODUCTS: bool = os.getenv("UPDATE_EXISTING_PRODUCTS", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("SCRAPER_LOG_LEVEL", "INFO")


config = ScraperConfig()
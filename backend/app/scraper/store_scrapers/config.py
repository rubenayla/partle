"""
Configuration management for the scraper.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from root .env file
root_env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '.env')
load_dotenv(root_env_path, override=True)


class ScraperConfig:
    """Configuration class for scraper settings."""
    
    # Database settings - Load from .env file
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # API settings (fallback for testing)
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    # Default user ID for scraped products (system user)
    DEFAULT_CREATOR_ID: Optional[int] = int(os.getenv("SCRAPER_USER_ID", "1")) if os.getenv("SCRAPER_USER_ID") else None
    
    # Store IDs mapping
    STORE_IDS = {
        "bricodepot": int(os.getenv("BRICODEPOT_STORE_ID", "3165")),  # Updated to canonical store ID
        "bauhaus": int(os.getenv("BAUHAUS_STORE_ID", "4065")),  # New Bauhaus store  
        "rationalstock": int(os.getenv("RATIONALSTOCK_STORE_ID", "4066")),  # Industrial supplier
        "leroy_merlin": int(os.getenv("LEROY_MERLIN_STORE_ID", "4067")),
        "ferreterias": int(os.getenv("FERRETERIAS_STORE_ID", "4068")),
        "ferreteria_shop": int(os.getenv("FERRETERIA_SHOP_STORE_ID", "4069")),
        "mengual": int(os.getenv("MENGUAL_STORE_ID", "4070")),  # Spanish hardware store
    }
    
    # Scraping behavior
    ENABLE_DUPLICATE_FILTER: bool = os.getenv("ENABLE_DUPLICATE_FILTER", "true").lower() == "true"
    UPDATE_EXISTING_PRODUCTS: bool = os.getenv("UPDATE_EXISTING_PRODUCTS", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("SCRAPER_LOG_LEVEL", "INFO")


config = ScraperConfig()
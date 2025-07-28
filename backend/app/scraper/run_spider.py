#!/usr/bin/env python3
"""
Cron-friendly wrapper script for running Scrapy spiders.

This script provides a reliable way to run scrapers from cron jobs with
proper logging, error handling, and status reporting.

Usage:
    python run_spider.py <spider_name> [options]
    
Examples:
    python run_spider.py bricodepot
    python run_spider.py bricodepot --log-level=DEBUG
    python run_spider.py bricodepot --resume
"""

import sys
import os
import logging
import argparse
from datetime import datetime
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from store_scrapers.config import config


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """Set up logging configuration."""
    log_format = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
    
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Default log file if not specified
    if not log_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = logs_dir / f"scraper_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return str(log_file)


def validate_spider(spider_name: str) -> bool:
    """Validate that the spider exists."""
    spider_dir = Path(__file__).parent / "store_scrapers" / "spiders"
    spider_file = spider_dir / f"{spider_name}.py"
    return spider_file.exists()


def run_spider(spider_name: str, **kwargs):
    """Run a spider with the given configuration."""
    logger = logging.getLogger(__name__)
    
    if not validate_spider(spider_name):
        logger.error(f"Spider '{spider_name}' not found")
        return False
    
    try:
        # Get Scrapy settings
        settings = get_project_settings()
        
        # Override settings with command line options
        if kwargs.get('log_level'):
            settings.set('LOG_LEVEL', kwargs['log_level'].upper())
        
        # Set up job directory for resumable crawls
        if kwargs.get('resume', True):  # Default to resumable
            crawl_state_dir = Path(__file__).parent / "crawls" / f"{spider_name}_crawl_state"
            crawl_state_dir.mkdir(parents=True, exist_ok=True)
            settings.set('JOBDIR', str(crawl_state_dir))
        
        # Create and configure the crawler process
        process = CrawlerProcess(settings)
        
        logger.info(f"Starting spider: {spider_name}")
        logger.info(f"Database URL: {config.DATABASE_URL}")
        logger.info(f"Duplicate filter enabled: {config.ENABLE_DUPLICATE_FILTER}")
        logger.info(f"Update existing products: {config.UPDATE_EXISTING_PRODUCTS}")
        
        # Start the spider
        process.crawl(spider_name)
        process.start()
        
        logger.info(f"Spider '{spider_name}' completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error running spider '{spider_name}': {e}", exc_info=True)
        return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Run Scrapy spiders with cron-friendly logging and error handling"
    )
    parser.add_argument(
        "spider", 
        help="Name of the spider to run (e.g., 'bricodepot', 'leroy_merlin')"
    )
    parser.add_argument(
        "--log-level", 
        default=config.LOG_LEVEL,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: %(default)s)"
    )
    parser.add_argument(
        "--log-file", 
        help="Path to log file (default: auto-generated in logs/ directory)"
    )
    parser.add_argument(
        "--no-resume", 
        action="store_true",
        help="Disable resumable crawls (start fresh each time)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Run without actually saving to database (for testing)"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    log_file = setup_logging(args.log_level, args.log_file)
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting scraper run - Log file: {log_file}")
    logger.info(f"Arguments: {vars(args)}")
    
    # Set environment variables for dry run
    if args.dry_run:
        os.environ["ENABLE_DUPLICATE_FILTER"] = "false"
        os.environ["UPDATE_EXISTING_PRODUCTS"] = "false"
        logger.info("DRY RUN MODE: No changes will be made to the database")
    
    # Run the spider
    success = run_spider(
        args.spider,
        log_level=args.log_level,
        resume=not args.no_resume,
        dry_run=args.dry_run
    )
    
    if success:
        logger.info("Scraper completed successfully")
        sys.exit(0)
    else:
        logger.error("Scraper failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
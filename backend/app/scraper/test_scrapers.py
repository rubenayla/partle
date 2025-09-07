#!/usr/bin/env python3
"""
Test all scrapers to check their current status
"""

import subprocess
import json
import time
from datetime import datetime

def test_scraper(spider_name, max_items=5):
    """Test a single scraper with limited items"""
    print(f"\n{'='*60}")
    print(f"Testing {spider_name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    cmd = [
        "scrapy", "crawl", spider_name,
        "-L", "INFO",  # Log level
        "-s", f"CLOSESPIDER_ITEMCOUNT={max_items}",  # Limit items
        "-s", "DOWNLOAD_TIMEOUT=10",  # Quick timeout
        "-s", "RETRY_TIMES=1",  # Minimal retries
        "-s", "CONCURRENT_REQUESTS=1",  # Single request at a time
        "-s", "DOWNLOAD_DELAY=1",  # 1 second delay
    ]
    
    try:
        # Run the scraper
        result = subprocess.run(
            cmd,
            cwd="/home/rubenayla/repos/partle/backend/app/scraper/store_scrapers",
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout per spider
        )
        
        # Check for success indicators
        output = result.stdout + result.stderr
        
        # Count items scraped
        items_scraped = output.count("'pipeline/items_created'")
        items_updated = output.count("'pipeline/items_updated'")
        errors = output.count("ERROR")
        warnings = output.count("WARNING")
        
        # Check for specific blocking indicators
        blocked_indicators = [
            "403", "429", "Forbidden", "Access Denied", "Blocked",
            "Cloudflare", "captcha", "robot", "bot detected"
        ]
        
        is_blocked = any(indicator.lower() in output.lower() for indicator in blocked_indicators)
        
        # Summary
        status = "❌ BLOCKED" if is_blocked else ("✅ WORKING" if items_scraped > 0 else "⚠️ NO ITEMS")
        
        print(f"\nStatus: {status}")
        print(f"Items created: {items_scraped}")
        print(f"Items updated: {items_updated}") 
        print(f"Errors: {errors}")
        print(f"Warnings: {warnings}")
        
        if is_blocked:
            print("Blocking detected - may need proxy or user-agent rotation")
            
        # Show sample of errors if any
        if errors > 0:
            error_lines = [line for line in output.split('\n') if 'ERROR' in line][:3]
            print("\nSample errors:")
            for line in error_lines:
                print(f"  {line[:150]}...")
                
        return {
            "spider": spider_name,
            "status": status,
            "items_scraped": items_scraped,
            "items_updated": items_updated,
            "errors": errors,
            "blocked": is_blocked
        }
        
    except subprocess.TimeoutExpired:
        print(f"⏱️ TIMEOUT - Spider took too long")
        return {
            "spider": spider_name,
            "status": "⏱️ TIMEOUT",
            "items_scraped": 0,
            "errors": 0,
            "blocked": False
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {
            "spider": spider_name,
            "status": "❌ ERROR",
            "items_scraped": 0,
            "errors": 1,
            "blocked": False
        }

def main():
    # Priority scrapers to test
    priority_spiders = [
        "leroy_merlin",
        "bricodepot",
        "bricodepot_simple",
        "bauhaus",
        "mengual",
        "rationalstock"
    ]
    
    results = []
    
    print("\n" + "="*60)
    print("SPANISH RETAILER SCRAPER TEST SUITE")
    print("="*60)
    
    for spider in priority_spiders:
        result = test_scraper(spider)
        results.append(result)
        time.sleep(2)  # Wait between tests
    
    # Summary report
    print("\n" + "="*60)
    print("SUMMARY REPORT")
    print("="*60)
    
    working = [r for r in results if "WORKING" in r["status"]]
    blocked = [r for r in results if "BLOCKED" in r["status"]]
    failed = [r for r in results if r["status"] not in ["✅ WORKING", "❌ BLOCKED"]]
    
    print(f"\n✅ Working scrapers ({len(working)}):")
    for r in working:
        print(f"  - {r['spider']}: {r['items_scraped']} items")
    
    print(f"\n❌ Blocked scrapers ({len(blocked)}):")
    for r in blocked:
        print(f"  - {r['spider']}")
    
    print(f"\n⚠️ Failed/No items ({len(failed)}):")
    for r in failed:
        print(f"  - {r['spider']}: {r['status']}")
    
    # Recommendations
    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    
    if blocked:
        print("\nFor blocked scrapers, consider:")
        print("  1. Implementing rotating user agents")
        print("  2. Adding proxy support")
        print("  3. Increasing delays between requests")
        print("  4. Using Playwright/Selenium for JavaScript sites")
    
    if failed:
        print("\nFor failed scrapers, check:")
        print("  1. Website structure changes")
        print("  2. Selector updates needed")
        print("  3. Store ID configuration")
        print("  4. URL format changes")

if __name__ == "__main__":
    main()
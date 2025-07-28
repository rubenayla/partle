#!/usr/bin/env python3
"""
Quick debug script to check PCComponentes structure.
"""

import asyncio
from playwright.async_api import async_playwright


async def debug_pccomponentes():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        )
        
        page = await browser.new_page()
        
        try:
            print("🔍 Checking PCComponentes.com structure...")
            await page.goto("https://www.pccomponentes.com/", timeout=15000)
            
            # Check for categories
            print("\n📋 Looking for category navigation...")
            nav_selectors = [
                'nav a', '.menu a', '.navigation a', 
                'li a[href*="categoria"]', 'a[href*="/c/"]'
            ]
            
            for selector in nav_selectors:
                elements = await page.query_selector_all(selector)
                if elements and len(elements) > 5:
                    print(f"✅ Found navigation with '{selector}': {len(elements)} links")
                    
                    # Sample some category links
                    for elem in elements[:5]:
                        href = await elem.get_attribute('href')
                        text = await elem.text_content()
                        if href and text and len(text.strip()) > 2:
                            print(f"   {text.strip()[:30]} -> {href[:50]}")
                    break
            
            # Try a specific category
            print(f"\n🔍 Testing a category page...")
            category_url = "https://www.pccomponentes.com/componentes"
            await page.goto(category_url, timeout=15000)
            
            # Look for product listings
            product_selectors = [
                '.product a', '[class*="product"] a', '.item a',
                'a[href*="/p/"]', 'a[data-cy*="product"]'
            ]
            
            for selector in product_selectors:
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"✅ Product selector '{selector}' found {len(elements)} links")
                    for elem in elements[:3]:
                        href = await elem.get_attribute('href')
                        text = await elem.text_content()
                        if href and text:
                            print(f"   {text.strip()[:40]} -> {href[:60]}")
                    if len(elements) > 10:  # Looks like product listings
                        break
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_pccomponentes())
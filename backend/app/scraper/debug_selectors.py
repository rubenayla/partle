#!/usr/bin/env python3
"""
Debug script to check what HTML structure Bricodepot actually has.
"""

import asyncio
from playwright.async_api import async_playwright


async def debug_bricodepot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--single-process',
            ]
        )
        
        page = await browser.new_page()
        
        try:
            print("🔍 Loading homepage...")
            await page.goto("https://www.bricodepot.es/", wait_until='domcontentloaded', timeout=30000)
            
            print("\\n📋 Looking for navigation/category links...")
            
            # Try different selectors for category links
            selectors_to_try = [
                'a.hm-link.main-navbar--item-parent',
                'a[href*="/"]',
                'nav a',
                '.navigation a',
                '.menu a',
                'a[class*="nav"]',
                'a[class*="menu"]',
                'a[class*="category"]'
            ]
            
            for selector in selectors_to_try:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        hrefs = []
                        for elem in elements[:5]:  # First 5 only
                            href = await elem.get_attribute('href')
                            text = await elem.text_content()
                            if href and text:
                                hrefs.append(f"{text.strip()[:30]} -> {href}")
                        
                        if hrefs:
                            print(f"\\n✅ Selector '{selector}' found {len(elements)} links:")
                            for href in hrefs:
                                print(f"   {href}")
                except Exception as e:
                    print(f"❌ Selector '{selector}' failed: {e}")
            
            # Try to visit a potential category page
            print("\\n🔍 Trying to find a category page...")
            category_links = await page.query_selector_all('a[href*="construccion"], a[href*="jardin"], a[href*="herramientas"]')
            
            if category_links:
                category_href = await category_links[0].get_attribute('href')
                full_url = f"https://www.bricodepot.es{category_href}" if category_href.startswith('/') else category_href
                
                print(f"🔍 Loading category page: {full_url}")
                await page.goto(full_url, wait_until='domcontentloaded', timeout=30000)
                
                print("\\n📦 Looking for product links...")
                product_selectors = [
                    'a.product-item-link',
                    'a[href*="product"]',
                    'a[class*="product"]',
                    '.product a',
                    '.item a',
                    'a[href*=".html"]'
                ]
                
                for selector in product_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        if elements:
                            print(f"\\n✅ Product selector '{selector}' found {len(elements)} links:")
                            for elem in elements[:3]:  # First 3 only
                                href = await elem.get_attribute('href')
                                text = await elem.text_content()
                                if href:
                                    print(f"   {text.strip()[:40] if text else 'No text'} -> {href[:60]}")
                            break
                    except Exception as e:
                        print(f"❌ Product selector '{selector}' failed: {e}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_bricodepot())
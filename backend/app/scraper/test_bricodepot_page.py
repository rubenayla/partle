#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def analyze_bricodepot_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("Loading Brico Depot category page...")
        await page.goto('https://www.bricodepot.es/decoracion-iluminacion', wait_until='domcontentloaded')
        
        # Wait a moment for dynamic content
        await page.wait_for_timeout(5000)
        
        # Get page title
        title = await page.title()
        print(f"Page title: {title}")
        
        # Look for product links with various selectors
        selectors_to_test = [
            'a[href*="/productos/"]',
            'a[href*="/product/"]',
            '.product-item a',
            '.product-link',
            '.product-name a',
            'a[href*=".html"]',
            '.algolia-hit a',
            '.ais-Hits-item a',
            '[data-objectid] a',
            '.search-results a',
            '.category-products a'
        ]
        
        for selector in selectors_to_test:
            links = await page.locator(selector).all()
            if links:
                print(f"\n=== Selector: {selector} ===")
                print(f"Found {len(links)} links")
                
                # Get first few links as examples
                for i, link in enumerate(links[:5]):
                    try:
                        href = await link.get_attribute('href')
                        text = await link.inner_text()
                        print(f"  Link {i+1}: {text[:50]}... -> {href}")
                    except:
                        print(f"  Link {i+1}: [Error getting link info]")
        
        # Also check if there are any obvious product containers
        print("\n=== Looking for product containers ===")
        containers_to_test = [
            '.product',
            '.product-item',
            '.item',
            '.algolia-hit',
            '.ais-Hits-item',
            '[data-objectid]',
            '.hit'
        ]
        
        for selector in containers_to_test:
            elements = await page.locator(selector).all()
            if elements:
                print(f"Found {len(elements)} elements matching: {selector}")
        
        # Get a sample of the page HTML to understand structure
        print("\n=== Page HTML sample ===")
        body_html = await page.locator('body').innerHTML()
        print(f"Body HTML length: {len(body_html)} characters")
        
        # Look for any form of product listing
        if 'algolia' in body_html.lower():
            print("Found 'algolia' in HTML - likely using Algolia search")
        if 'product' in body_html.lower():
            print("Found 'product' references in HTML")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(analyze_bricodepot_page())
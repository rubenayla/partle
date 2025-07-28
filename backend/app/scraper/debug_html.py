#!/usr/bin/env python3
"""
Debug script to save actual HTML and see what's on the category page.
"""

import asyncio
from playwright.async_api import async_playwright


async def save_html():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--single-process']
        )
        
        page = await browser.new_page()
        
        try:
            # Try different category pages
            urls_to_try = [
                "https://www.bricodepot.es/herramientas/herramientas-manuales",
                "https://www.bricodepot.es/construccion/materiales-construccion",
                "https://www.bricodepot.es/jardin/muebles"
            ]
            
            for url in urls_to_try:
                print(f"🔍 Loading: {url}")
                await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                
                # Wait for any JS to load
                await page.wait_for_timeout(5000)
                
                # Look for common product listing indicators
                indicators = [
                    '.product',
                    '[class*="product"]',
                    '.item',
                    '[class*="item"]',
                    '.card',
                    '[data-*="product"]',
                    '.listing',
                    '.grid'
                ]
                
                print(f"\\n📦 Checking for product containers...")
                found_containers = []
                
                for indicator in indicators:
                    try:
                        elements = await page.query_selector_all(indicator)
                        if elements and len(elements) > 5:  # Likely product listings have multiple items
                            found_containers.append((indicator, len(elements)))
                    except:
                        pass
                
                if found_containers:
                    print(f"✅ Found potential product containers:")
                    for selector, count in found_containers[:5]:
                        print(f"   {selector}: {count} elements")
                        
                        # Check what's inside these containers
                        container = await page.query_selector(selector)
                        if container:
                            links = await container.query_selector_all('a[href]')
                            if links:
                                for link in links[:2]:
                                    href = await link.get_attribute('href')
                                    text = await link.text_content()
                                    if href and text and len(text.strip()) > 5:
                                        print(f"      Link: {text.strip()[:40]} -> {href[:60]}")
                else:
                    print("❌ No obvious product containers found")
                
                # Save a snippet of HTML to see structure
                html_snippet = await page.content()
                filename = f"debug_{url.split('/')[-1]}.html"
                
                # Save first 50KB of HTML
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_snippet[:50000])
                print(f"💾 Saved HTML snippet to {filename}")
                
                print("="*70)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(save_html())
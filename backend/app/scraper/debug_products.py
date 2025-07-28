#!/usr/bin/env python3
"""
Debug script to find actual product links on Bricodepot category pages.
"""

import asyncio
from playwright.async_api import async_playwright


async def find_products():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--single-process']
        )
        
        page = await browser.new_page()
        
        try:
            # Go to a specific category that should have products
            category_url = "https://www.bricodepot.es/herramientas/herramientas-manuales"
            print(f"🔍 Loading category: {category_url}")
            await page.goto(category_url, wait_until='domcontentloaded', timeout=30000)
            
            # Wait a bit for any JS to load products
            await page.wait_for_timeout(3000)
            
            print("\\n📦 Looking for individual product links...")
            
            # Try to find patterns that look like individual products
            all_links = await page.query_selector_all('a[href]')
            print(f"Found {len(all_links)} total links")
            
            product_candidates = []
            for link in all_links:
                href = await link.get_attribute('href')
                text = await link.text_content()
                
                if href and text:
                    text = text.strip()
                    # Look for links that might be individual products
                    if (len(text) > 10 and len(text) < 100 and  # Reasonable product name length
                        not href.startswith('#') and  # Not anchor links
                        not 'categoria' in href.lower() and  # Not category links
                        not 'category' in href.lower() and
                        not '/media/' in href and  # Not image links
                        not text.lower() in ['ver más', 'ver todo', 'siguiente', 'anterior', 'página'] and
                        href.count('/') >= 3):  # Looks like a deeper product URL
                        
                        product_candidates.append((text[:50], href))
            
            print(f"\\n🎯 Found {len(product_candidates)} potential product links:")
            for i, (text, href) in enumerate(product_candidates[:10], 1):
                print(f"{i:2d}. {text:<50} -> {href}")
            
            # Try to visit one product page to see what selectors work
            if product_candidates:
                product_url = product_candidates[0][1]
                if not product_url.startswith('http'):
                    product_url = f"https://www.bricodepot.es{product_url}"
                
                print(f"\\n🔍 Testing product page: {product_url}")
                try:
                    await page.goto(product_url, wait_until='domcontentloaded', timeout=30000)
                    await page.wait_for_timeout(2000)
                    
                    # Test product data selectors
                    selectors_to_test = {
                        'name': ['h1.product-name', 'h1', '.product-name', '[class*="product"] h1', '.title h1'],
                        'price': ['span.price', '.price', '[class*="price"]', '.precio'],
                        'image': ['img.product-image-photo', '.product-image img', '.gallery img', 'img[src*="product"]'],
                        'description': ['div.product-description-content p', '.description', '.product-description']
                    }
                    
                    print("\\n🧪 Testing product data selectors:")
                    for data_type, selectors in selectors_to_test.items():
                        print(f"\\n{data_type.upper()}:")
                        for selector in selectors:
                            try:
                                element = await page.query_selector(selector)
                                if element:
                                    if data_type == 'image':
                                        value = await element.get_attribute('src')
                                    else:
                                        value = await element.text_content()
                                    
                                    if value:
                                        print(f"  ✅ {selector}: {value.strip()[:60]}...")
                                        break
                                else:
                                    print(f"  ❌ {selector}: not found")
                            except Exception as e:
                                print(f"  ❌ {selector}: error - {e}")
                
                except Exception as e:
                    print(f"❌ Could not load product page: {e}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(find_products())
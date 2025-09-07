#!/usr/bin/env python3
"""
Test Rationalstock image extraction
"""
import scrapy
from scrapy.crawler import CrawlerProcess

class TestImageSpider(scrapy.Spider):
    name = "test_image"
    start_urls = [
        # Direct product URL
        "https://www.rationalstock.es/catalogo/producto/herramientas/herramientas-abrasivas/discos-abrasivos-flexibles/disco-abrasivo-con-soporte-de-fibra-y-mineral-de-corindon-ceramico-ref--ca-p93-v/10055000024"
    ]
    
    def parse(self, response):
        # Test different image extraction methods
        print("\n" + "="*60)
        print("TESTING IMAGE EXTRACTION ON:", response.url)
        print("="*60)
        
        # Method 1: Meta itemprop
        img1 = response.css('meta[itemprop="image"]::attr(content)').get()
        print(f"1. Meta itemprop='image': {img1}")
        
        # Method 2: Open Graph
        img2 = response.css('meta[property="og:image"]::attr(content)').get()
        print(f"2. Meta og:image: {img2}")
        
        # Method 3: Twitter
        img3 = response.css('meta[name="twitter:image"]::attr(content)').get()
        print(f"3. Meta twitter:image: {img3}")
        
        # Method 4: Product name
        name = response.css('h1::text').get()
        print(f"\nProduct name: {name}")
        
        # Method 5: Price
        price = response.xpath('//*[contains(text(), "€")]/text()').get()
        print(f"Price text: {price}")
        
        print("="*60)
        
        if img1:
            yield {
                'name': name,
                'image_url': img1,
                'price': price
            }

# Run the test
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

process.crawl(TestImageSpider)
process.start()
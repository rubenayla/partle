"""
Scrapy spider for scraping hardware and DIY stores in Spain using Overpass API.

This spider queries the Overpass API to retrieve information about
"hardware" and "doityourself" shops within Spain, and then processes
the results to extract store details such as name, address, phone,
website, latitude, longitude, and tags.
"""

import scrapy
import json
from ..items import StoreScrapersItem


class FerreteriasSpider(scrapy.Spider):
    """
    Spider for scraping hardware stores (ferreterias) from OpenStreetMap via Overpass API.
    """
    name = 'ferreterias'
    overpass_url = 'https://overpass-api.de/api/interpreter'
    download_delay = 1  # Be courteous to the API by adding a delay between requests

    def start_requests(self):
        """
        Initiates the scraping process by sending a POST request to the Overpass API.
        The query targets hardware and DIY shops within Spain.
        """
        overpass_query = '''
[out:json][timeout:60];
area["ISO3166-1"="ES"][admin_level=2]->.es;
(
  nwr["shop"="hardware"](area.es);
  nwr["shop"="doityourself"](area.es);
);
out tags center;
'''
        yield scrapy.Request(
            url=self.overpass_url,
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            body=f'data={overpass_query}',
            callback=self.parse
        )

    def parse(self, response):
        """
        Parses the JSON response from the Overpass API and extracts store information.

        Args:
            response (scrapy.http.Response): The response object containing the Overpass API JSON data.
        """
        data = json.loads(response.text)
        for element in data.get('elements', []):
            if 'tags' in element:
                item = StoreScrapersItem()
                item['name'] = element['tags'].get('name')

                # Construct address from available tags, prioritizing 'addr:full'
                address_parts = []
                if element['tags'].get('addr:full'):
                    address_parts.append(element['tags']['addr:full'])
                else:
                    if element['tags'].get('addr:street'):
                        address_parts.append(element['tags']['addr:street'])
                    if element['tags'].get('addr:housenumber'):
                        address_parts.append(element['tags']['addr:housenumber'])
                    if element['tags'].get('addr:postcode'):
                        address_parts.append(element['tags']['addr:postcode'])
                    if element['tags'].get('addr:city'):
                        address_parts.append(element['tags']['addr:city'])
                item['address'] = ', '.join(address_parts) if address_parts else None

                item['phone'] = element['tags'].get('phone')
                # Prioritize 'website' tag, fallback to 'url' tag
                item['website'] = element['tags'].get('website') or element['tags'].get('url')
                item['latitude'] = element.get('lat')
                item['longitude'] = element.get('lon')
                item['tags'] = ['Ferreteria']  # Tag all scraped items as 'Ferreteria'

                yield item

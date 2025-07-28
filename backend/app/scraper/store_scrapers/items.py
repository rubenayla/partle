# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    """Item for scraped product data."""
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    store_id = scrapy.Field()
    spec = scrapy.Field()  # Optional specification field


class StoreScrapersItem(scrapy.Item):
    """Legacy item for store data - kept for backward compatibility."""
    name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    tags = scrapy.Field()

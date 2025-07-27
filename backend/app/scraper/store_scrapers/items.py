# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StoreScrapersItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    tags = scrapy.Field()

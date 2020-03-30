# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst,Identity
import re

def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'
    return value

def cleaner_price(value):
    #r=re.sub(r'\D', '', value)
    return re.sub(r'\D', '', value)

def cleaner_prop1(value):
    return re.sub(r'\n', '', value)

def cleaner_prop2(value):
    return re.sub(r'\n| ', '', value)

class LeroyParserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(input_processor=MapCompose(cleaner_price))
    pr_h = scrapy.Field(input_processor=MapCompose(cleaner_prop1))
    pr_p = scrapy.Field(input_processor=MapCompose(cleaner_prop2))
    props = scrapy.Field()
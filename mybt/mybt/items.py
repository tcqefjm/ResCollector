# -*- coding: utf-8 -*-

import scrapy

class MybtItem(scrapy.Item):
    name = scrapy.Field()
    source = scrapy.Field()
    link = scrapy.Field()
    size = scrapy.Field()
    seeder = scrapy.Field()
    leecher = scrapy.Field()
    site = scrapy.Field()

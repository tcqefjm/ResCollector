# -*- coding: utf-8 -*-

from BtCollector.models import BtCollector
from scrapy_djangoitem import DjangoItem
import scrapy

class MybtItem(DjangoItem):
    django_model = BtCollector
    name = scrapy.Field()
    source = scrapy.Field()
    link = scrapy.Field()
    size = scrapy.Field()
    seeder = scrapy.Field()
    leecher = scrapy.Field()
    site = scrapy.Field()
    search = scrapy.Field()
    cat = scrapy.Field()
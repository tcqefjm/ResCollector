# -*- coding: utf-8 -*-

from BtCollector.models import BtCollector
from scrapy_djangoitem import DjangoItem
import scrapy

class MybtItem(DjangoItem):
    django_model = BtCollector
    name = scrapy.Field() #资源名称
    source = scrapy.Field() #资源原始页面
    link = scrapy.Field() #资源下载地址
    size = scrapy.Field() #资源大小
    seeder = scrapy.Field() #做种数
    leecher = scrapy.Field() #下载数
    site = scrapy.Field() #来源站点
    search = scrapy.Field() #搜索字段
    cat = scrapy.Field() #搜索种类

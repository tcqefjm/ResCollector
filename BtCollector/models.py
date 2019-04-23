from django.db import models

class BtCollector(models.Model):
    name = models.CharField(max_length = 255) #资源名称
    source = models.URLField() #资源原始页面
    link = models.TextField() #资源下载地址
    size = models.CharField(max_length = 15) #资源大小
    seeder = models.PositiveIntegerField() #做种数
    leecher = models.PositiveIntegerField() #下载数
    site = models.CharField(max_length = 15) #来源站点
    search = models.CharField(max_length = 63) #搜索字段
    cat = models.CharField(max_length = 15, default = 'all') #搜索种类

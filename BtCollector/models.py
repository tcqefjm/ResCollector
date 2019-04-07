from django.db import models

class BtCollector(models.Model):
    name = models.CharField(max_length = 255)
    source = models.URLField()
    link = models.TextField()
    size = models.CharField(max_length = 15)
    seeder = models.PositiveIntegerField()
    leecher = models.PositiveIntegerField()
    site = models.CharField(max_length = 15)
    search = models.CharField(max_length = 63)
    cat = models.CharField(max_length = 15, default = 'all')
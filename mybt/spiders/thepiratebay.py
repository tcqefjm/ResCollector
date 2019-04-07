from scrapy import Spider
from mybt.items import MybtItem

class ThePirateBay(Spider):
	name = 'thepiratebay'
	category = {
		'all': '0',
		'music': '100',
		'movies': '200',
		'tv': '200',
		'software': '300',
		'games': '400',
		'books': '601'
	}
	
	def __init__(self, search, cat = "all", **kwargs):
		super(ThePirateBay, self).__init__()
		self.start_urls = [
			'https://pirateproxy.live/search/{search}/1/7/{cat}'.format(search = search, cat = self.category[cat]),
			'https://pirateproxy.live/search/{search}/2/7/{cat}'.format(search = search, cat = self.category[cat])
		]
		self.search = search
		self.cat = cat

	def parse(self, response):
		item = MybtItem()
		results = response.xpath('//table/tr')[:-1]
		for result in results:
			item['name'] = result.xpath('./td[2]/div/a/text()').extract()[0]
			item['source'] = result.xpath('./td[2]/div/a/@href').extract()[0]
			item['link'] = result.xpath('./td[2]/a/@href').extract()[0]
			item['size'] = result.xpath('./td[2]/font/text()').extract()[0]
			item['size'] = item['size'].split(', ')[1].lstrip('Size ').replace('i', '').replace('\xa0', ' ')
			item['seeder'] = result.xpath('./td[3]/text()').extract()[0]
			item['leecher'] = result.xpath('./td[4]/text()').extract()[0]
			item['site'] = 'ThePirateBay'
			item['search'] = self.search
			item['cat'] = self.cat
			if int(item['seeder']):
				yield item

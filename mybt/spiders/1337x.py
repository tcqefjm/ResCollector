from scrapy import Spider, Request
from mybt.items import MybtItem

class LeetX(Spider):
	name = '1337x'
	category = {
		'all': 'All',
		'movies': 'Movies',
		'tv': 'TV',
		'music': 'Music',
		'games': 'Games',
		'anime': 'Anime',
		'software': 'Apps'
	}
	
	def __init__(self, search, cat = "all", **kwargs):
		super(LeetX, self).__init__()
		self.start_urls = [
			'https://1337x.to/search/{search}/1/'.format(search = search) if cat == "all" else \
			'https://1337x.to/category-search/{search}/{cat}/1/'.format(search = search, cat = self.category[cat]),
			'https://1337x.to/search/{search}/2/'.format(search = search) if cat == "all" else \
			'https://1337x.to/category-search/{search}/{cat}/2/'.format(search = search, cat = self.category[cat]),
			'https://1337x.to/search/{search}/3/'.format(search = search) if cat == "all" else \
			'https://1337x.to/category-search/{search}/{cat}/3/'.format(search = search, cat = self.category[cat])
		]
		self.search = search
		self.cat = cat

	def parse(self, response):
		results = response.xpath('//table/tbody/tr')
		for result in results:
			item = MybtItem()
			item['name'] = result.xpath('./td[@class="coll-1 name"]/a[2]/text()').extract()[0]
			item['source'] = result.xpath('./td[@class="coll-1 name"]/a[2]/@href').extract()
			item['source'] = 'https://1337x.to' + item['source'][0]
			yield Request(url = item['source'], meta = {'item': item}, callback = self.secondParse)
	
	def secondParse(self, response):
		item = response.meta['item']
		detail = response.xpath('//div[@class="torrent-category-detail clearfix"]')
		item['link'] = detail.xpath('./ul[1]/li[1]/a/@href').extract()[0]
		item['size'] = detail.xpath('./ul[2]/li[4]/span/text()').extract()[0]
		item['seeder'] = detail.xpath('./ul[3]/li[4]/span/text()').extract()[0]
		item['leecher'] = detail.xpath('./ul[3]/li[5]/span/text()').extract()[0]
		item['site'] = '1337X'
		item['search'] = self.search
		item['cat'] = self.cat
		if int(item['seeder']):
			yield item

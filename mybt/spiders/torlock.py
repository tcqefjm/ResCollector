from scrapy import Spider, Request
from mybt.items import MybtItem

class TORLOCK(Spider):
	name = 'torlock'
	category = {
		'all': 'all',
		'anime': 'anime',
		'software': 'software',
		'games': 'game',
		'movies': 'movie',
		'music': 'music',
		'tv': 'television',
		'books': 'ebook'
	}
	
	def __init__(self, search, cat = "all", **kwargs):
		super(TORLOCK, self).__init__()
		search = search.replace(' ', '-')
		cat = self.category[cat]
		self.start_urls = [
			'https://www.torlock.com/{cat}/torrents/{search}.html?sort=seeds'.format(cat = cat, search = search)
		]
		self.search = search
		self.cat = cat

	def parse(self, response):
		results = response.xpath('//div[@class="panel panel-default"]/table/tr')
		for result in results:
			item = MybtItem()
			item['name'] = result.xpath('string(./td[1]//b)').extract()[0]
			item['source'] = result.xpath('./td[1]//a/@href').extract()
			item['source'] = 'https://www.torlock.com' + item['source'][0]
			item['size'] = result.xpath('./td[3]/text()').extract()[0]
			item['seeder'] = result.xpath('./td[4]/text()').extract()[0]
			item['leecher'] = result.xpath('./td[5]/text()').extract()[0]
			if int(item['seeder']):
				yield Request(url = item['source'], meta = {'item': item}, callback = self.secondParse)

	def secondParse(self, response):
		item = response.meta['item']
		item['link'] = response.xpath('//div[@style="float:right;padding-right:5px"]//a[1]/@href').extract()[0]
		item['site'] = 'TORLOCK'
		item['search'] = self.search
		item['cat'] = self.cat
		yield item

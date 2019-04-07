from scrapy import Spider, Request
from mybt.items import MybtItem

class LimeTorrents(Spider):
	name = 'limetorrents'
	category = {
		'all': 'all',
		'anime': 'anime',
		'software': 'applications',
		'games': 'games',
		'movies': 'movies',
		'music': 'music',
		'tv': 'tv'
	}
	
	def __init__(self, search, cat = "all", **kwargs):
		super(LimeTorrents, self).__init__()
		search = search.replace(' ', '-')
		cat = self.category[cat]
		self.start_urls = [
			'https://www.limetorrents.info/search/{cat}/{search}/seeds/1/'.format(cat = cat, search = search)
		]
		self.search = search
		self.cat = cat

	def parse(self, response):
		results = response.xpath('//table[@class="table2"]/tr[@bgcolor]')
		for result in results:
			item = MybtItem()
			item['name'] = result.xpath('.//div[@class="tt-name"]/a[2]/text()').extract()[0]
			item['source'] = result.xpath('.//div[@class="tt-name"]/a[2]/@href').extract()
			item['source'] = 'https://www.limetorrents.info' + item['source'][0]
			yield Request(url = item['source'], meta = {'item': item}, callback = self.secondParse)
	
	def secondParse(self, response):
		item = response.meta['item']
		item['link'] = response.xpath('//div[@class="torrentinfo"]/div[@class="downloadarea"][2]//p/a/@href').extract()[0]
		item['size'] = response.xpath('//div[@class="torrentinfo"]/table/tr[3]/td[2]/text()').extract()[0]
		item['seeder'] = response.xpath('//div[@id="content"]/span[@class="greenish"]/text()').extract()[0].lstrip('Seeders : ')
		item['leecher'] = response.xpath('//div[@id="content"]/span[@class="reddish"]/text()').extract()[0].lstrip('Leechers : ')
		item['site'] = 'LimeTorrents'
		item['search'] = self.search
		item['cat'] = self.cat
		if int(item['seeder']):
			yield item

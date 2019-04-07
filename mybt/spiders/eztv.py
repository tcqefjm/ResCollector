from scrapy import Spider, Request
from mybt.items import MybtItem

class EZTV(Spider):
	name = 'eztv'
	category = {'tv': 'tv'}
	
	def __init__(self, search, cat = "tv", **kwargs):
		super(EZTV, self).__init__()
		self.start_urls = [
			'https://eztv.io/search/{search}'.format(search = search.replace(' ', '-'))
		]
		self.search = search
		self.cat = cat

	def parse(self, response):
		results = response.xpath('//table[@class="forum_header_border"]/tr[@class="forum_header_border"]')
		for result in results:
			item = MybtItem()
			item['name'] = result.xpath('./td[2]/a/text()').extract()[0].rstrip(' [eztv]')
			item['source'] = result.xpath('./td[2]/a/@href').extract()
			item['source'] = 'https://eztv.io' + item['source'][0]
			item['link'] = result.xpath('./td[3]/a[@class="magnet"]/@href').extract()[0]
			item['size'] = result.xpath('./td[4]/text()').extract()[0]
			yield Request(url = item['source'], meta = {'item': item}, callback = self.secondParse)
	
	def secondParse(self, response):
		item = response.meta['item']
		item['seeder'] = response.xpath('//td[@style="padding-left: 5px;"]/span[1]/text()').extract()[0].replace(',', '')
		item['leecher'] = response.xpath('//td[@style="padding-left: 5px;"]/span[2]/text()').extract()[0].replace(',', '')
		item['site'] = 'EZTV'
		item['search'] = self.search
		item['cat'] = self.cat
		if int(item['seeder']):
			yield item

from scrapy import Spider
from mybt.items import MybtItem

class RUTOR(Spider):
	name = 'rutor'
	category = {
		'all': '0',
		'movies': '1',
		'music': '2',
		'tv': '4',
		'games': '8',
		'software': '9',
		'books': '11'
	}
	
	def __init__(self, search, cat = "all", **kwargs):
		super(RUTOR, self).__init__()
		self.start_urls = [
			'http://rutor.info/search/0/{cat}/000/2/{search}'.format(cat = self.category[cat], search = search)
		]
		self.search = search
		self.cat = cat

	def parse(self, response):
		item = MybtItem()
		results = response.xpath('//div[@id="index"]/table/tr')[1:]
		for result in results:
			item['name'] = result.xpath('./td[2]/a[3]/text()').extract()[0][:-1]
			item['source'] = result.xpath('./td[2]/a[3]/@href').extract()
			item['source'] = 'http://rutor.info' + item['source'][0]
			item['link'] = result.xpath('./td[2]/a[2]/@href').extract()[0]
			item['size'] = result.xpath('./td[last()-1]/text()').extract()[0].replace('\xa0', ' ')
			item['seeder'] = result.xpath('./td[last()]/span[1]/text()').extract()[0][1:]
			item['leecher'] = result.xpath('./td[last()]/span[2]/text()').extract()[0][1:]
			item['site'] = 'RUTOR'
			item['search'] = self.search
			item['cat'] = self.cat
			if int(item['seeder']):
				yield item

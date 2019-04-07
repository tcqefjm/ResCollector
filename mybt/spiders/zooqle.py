from scrapy import Spider
from mybt.items import MybtItem

class Zooqle(Spider):
	name = 'zooqle'
	category = {
		'all': 'all',
		'movies': 'Movies',
		'tv': 'TV',
		'music': 'Music',
		'games': 'Games',
		'anime': 'Anime',
		'software': 'Apps',
		'books': 'Books'
	}
	
	def __init__(self, search, cat = "all", **kwargs):
		super(Zooqle, self).__init__()
		self.start_urls = [
			'https://zooqle.com/search?q={search}+category%3A{cat}'.format(search = search, cat = self.category[cat])
		]
		self.search = search
		self.cat = cat

	def parse(self, response):
		item = MybtItem()
		results = response.xpath('//table/tr')
		for result in results:
			item['name'] = result.xpath('string(./td[2]/a[@class=" small"])').extract()[0]
			if not item['name']:
				continue
			item['source'] = result.xpath('./td[2]/a/@href').extract()
			item['source'] = 'https://zooqle.com' + item['source'][0]
			item['link'] = result.xpath('./td[3]/ul/li[2]/a/@href').extract()[0]
			item['size'] = result.xpath('./td[4]//text()').extract()[0]
			seeder_leecher = result.xpath('.//td[6]/div/@title').extract()[0].split(' | ')
			item['seeder'] = seeder_leecher[0].lstrip('Seeders: ')
			item['leecher'] = seeder_leecher[1].lstrip('Leechers: ')
			item['site'] = 'Zooqle'
			item['search'] = self.search
			item['cat'] = self.cat
			yield item

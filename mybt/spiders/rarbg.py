from scrapy import Spider, Request
from mybt.items import MybtItem
from json import loads
from urllib.parse import urlencode

class RARBG(Spider):
	name = 'rarbg'
	category = {
		'all': '1;4;14;15;16;17;21;22;42;18;19;41;27;28;29;30;31;32;40;23;24;25;26;33;34;43;44;45;46;47;48',
		'movies': 'movies',
		'tv': 'tv',
		'music': '1;23;24;25;26',
		'games': '1;27;28;29;30;31;32;40',
		'software': '1;33;34;43'
	}
	
	def __init__(self, search, cat = "all", **kwargs):
		super(RARBG, self).__init__()
		self.start_urls = [
			'https://torrentapi.org/pubapi_v2.php?get_token=get_token&app_id=mybt'
		]
		self.search = search
		self.category = self.category[cat]
		self.cat = cat

	def parse(self, response):
		token = loads(response.text)['token']
		url = 'https://torrentapi.org/pubapi_v2.php?'
		url += urlencode({
			'mode': 'search',
			'search_string': self.search,
			'category': self.category,
			'limit': 50,
			'sort': 'seeders',
			'format': 'json_extended',
			'ranked': 0,
			'token': token,
			'app_id': 'mybt'
		})
		yield Request(url = url, callback = self.secondParse)

	def secondParse(self, response):
		try:
			item = MybtItem()
			results = loads(response.text)['torrent_results']
			for result in results:
				item['name'] = result['title']
				item['source'] = result['info_page']
				item['link'] = result['download']
				item['size'] = sizeConvert(result['size'])
				item['seeder'] = result['seeders']
				item['leecher'] = result['leechers']
				item['site'] = 'RARBG'
				item['search'] = self.search
				item['cat'] = self.cat
				if item['seeder']:
					yield item
		except KeyError:
			pass

def sizeConvert(size):
	size_map = (
		(1 << 50, 'PB'),
		(1 << 40, 'TB'),
		(1 << 30, 'GB'),
		(1 << 20, 'MB'),
		(1 << 10, 'KB'),
		(1 << 0, 'B'),
	)
	for factor, suffix in size_map:
		if size >= factor:
			break
	return '{:.2f} {}'.format(size/factor, suffix)

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

support_category = {
	'all': ('1337x', 'limetorrents', 'rarbg', 'rutor', 'thepiratebay', 'torlock', 'zooqle'),
	'anime': ('1337x', 'limetorrents', 'torlock', 'zooqle'),
	'books': ('rutor', 'thepiratebay', 'torlock', 'zooqle'),
	'games': ('1337x', 'limetorrents', 'rarbg', 'rutor', 'thepiratebay', 'torlock', 'zooqle'),
	'movies': ('1337x', 'limetorrents', 'rarbg', 'rutor', 'thepiratebay', 'torlock', 'zooqle'),
	'music': ('1337x', 'limetorrents', 'rarbg', 'rutor', 'thepiratebay', 'torlock', 'zooqle'),
	'software': ('1337x', 'limetorrents', 'rarbg', 'rutor', 'thepiratebay', 'torlock', 'zooqle'),
	'tv': ('1337x', 'eztv', 'limetorrents', 'rarbg', 'rutor', 'thepiratebay', 'torlock', 'zooqle'),
}

def crawl(search, cat):
	process = CrawlerProcess(get_project_settings())
	for spider in support_category[cat]:
		process.crawl(spider, search = search, cat = cat)
	process.start()

crawl('the walking dead', 'all')
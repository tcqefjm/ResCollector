from scrapyd_api import ScrapydAPI
from django.shortcuts import render
from .models import BtCollector
from time import sleep

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

scrapyd = ScrapydAPI('http://localhost:6800')

last_query = ''

def search(request, search, cat):
	global last_query
	current_result = BtCollector.objects.filter(search = search, cat = cat)
	if not current_result or last_query == request.path:
		current_result.delete()
		for spider in support_category[cat]:
			task = scrapyd.schedule('default', spider, search = search, cat = cat)
		sleep(10)
	else:
		last_query = request.path

	results = BtCollector.objects.filter(search = search, cat = cat).order_by('-seeder', '-leecher')
	context = {'results': results, 'search': search}
	return render(request, 'BtCollector/search.html', context)

from scrapyd_api import ScrapydAPI
from django.shortcuts import render, redirect
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

def index(request):
	global last_query
	BtCollector.objects.all().delete()
	last_query = ''
	return render(request, 'BtCollector/bt_home.html')

def search(request, search, cat):
	global last_query
	if last_query != request.path:
		last_query = request.path
		results = BtCollector.objects.filter(search = search, cat = cat)
		if not results:
			for spider in support_category[cat]:
				task = scrapyd.schedule('default', spider, search = search, cat = cat)
			sleep(8)
	
	results = BtCollector.objects.filter(search = search, cat = cat).order_by('-seeder', '-leecher')
	context = {'results': results, 'search': search, 'cat': cat}
	return render(request, 'BtCollector/bt_result.html', context)

def to_search(request):
	try:
		search = request.GET['q']
		cat = request.GET['cat']
	except KeyError:
		return redirect('/bt/')
	if search and cat in support_category.keys():
		return redirect('/'.join(['/bt', cat, search]))
	else:
		return redirect('/bt/')

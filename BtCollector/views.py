from scrapyd_api import ScrapydAPI
from django.shortcuts import render, redirect
from .models import BtCollector
from time import sleep

#根据搜索种类调整调用的爬虫
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

scrapyd = ScrapydAPI('http://localhost:6800') #爬虫调度接口

last_query = '' #历史检索字段

#BT资源站首页
def index(request):
	global last_query
	BtCollector.objects.all().delete() #清空数据库
	last_query = '' #清空检索字段历史
	return render(request, 'BtCollector/bt_home.html')

#BT资源站搜索页面
def search(request, search, cat):
	global last_query
	#在搜索历史中检索是否存在有效的历史搜索记录
	#若存在，则直接提取从数据库中查询到的结果
	#若不存在，则通过爬虫调度接口启动爬虫，然后延时八秒搜索数据库
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

#搜索表单提交页
#自动跳转至搜索页面
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

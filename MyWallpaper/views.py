from django.http import HttpResponse
from threading import Thread
from random import randrange
from urllib.request import urlretrieve

def wallpaper(request):
	with open('./static/wallpaper.jpg', 'rb') as f:
		image = f.read();
	Thread(target = getWallpaper, daemon = True).start()
	return HttpResponse(image, content_type = 'image/jpeg')

def getWallpaper():
	try:
		url = 'http://img.infinitynewtab.com/wallpaper/{}.jpg'.format(randrange(2400,3000))
		urlretrieve(url, './static/wallpaper.jpg')
	except:
		pass

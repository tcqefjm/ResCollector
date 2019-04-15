from django.urls import path
from . import views

urlpatterns = [
	path('', views.wallpaper, name='wallpaper'),
]
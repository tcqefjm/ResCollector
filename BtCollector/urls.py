from django.urls import path
from . import views

urlpatterns = [
	path('<cat>/<search>/', views.search, name='search'),
	path('search/', views.to_search, name='search'),
	path('', views.index, name='index'),
]
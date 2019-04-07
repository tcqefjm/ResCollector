from django.urls import path
from . import views

urlpatterns = [
	path('<cat>/<search>/', views.search, name='search'),
]
from django.urls import path
from . import views

app_name = 'tinder'
urlpatterns = [
	#path('ola', views.match_withlist, name='match'),
	path('my_menu/', views.my_menu, name='main_menu'),
	path('group/create/', views.create_group, name='create_group'),
]
from django.urls import path
from . import views

app_name = 'tinder'
urlpatterns = [
	#path('ola', views.match_withlist, name='match'),
	path('my_menu/', views.my_menu, name='main_menu'),
	path('group/create/', views.create_group, name='create_group'),
	path('group/view/<int:group_id>', views.view_group, name='view_group'),
	path('group/edit/<int:group_id>', views.edit_group, name='edit_group'),
	path('group/search', views.search_group, name='search_group'),
]

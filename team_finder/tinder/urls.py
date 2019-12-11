from django.urls import path
from . import views

app_name = 'tinder'
urlpatterns = [
	#path('ola', views.match_withlist, name='match'),
	path('my_menu/', views.my_menu, name='main_menu'),
	path('group/create/', views.create_group, name='create_group'),
	path('group/<int:group_id>/edit/', views.edit_group, name='edit_group'),
	path('group/<int:pk>/', views.DetailGroup.as_view(), name='detail_group'),
	path('group/<int:pk>/activity/', views.activity_group_match, name='activity-group'),
	path('group/<int:group_id>/match/', views.match_withlist, name='match'),
]

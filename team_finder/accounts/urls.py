from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_account, name="register"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('profile/', views.review_account, name="profile"),
    path('profile/change_avatar/', views.change_avatar, name="change_avatar"),
]

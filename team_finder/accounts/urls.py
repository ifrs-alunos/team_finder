from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register_account, name="register"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/view/<int:pk>/', views.DetailProfile.as_view(), name="detail_profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
]

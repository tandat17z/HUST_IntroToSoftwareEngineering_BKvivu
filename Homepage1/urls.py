from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('homepage/<str:username>', views.home, name='home'),
    path('login/', views.login, name='login'),
]

from django.urls import path, include
from . import views


app_name = 'homepage'
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('login/', views.loginPage, name='loginPage'),
    path('login/register/', views.registerPage, name='registerPage'),
]
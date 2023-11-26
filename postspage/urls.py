from django.urls import path, include
from . import views


app_name = 'postspage'
urlpatterns = [
    path('', views.postsPage, name='postsPage'),
    
]
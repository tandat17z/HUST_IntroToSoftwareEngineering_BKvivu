from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.home, name='home'),
    path('members/details/<id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
    
]
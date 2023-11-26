from django.urls import path, include
from . import views

app_name = 'profilepage'
urlpatterns = [
    path('', views.profilePage, name='profilePage'),
    path('logout/', views.logout_view, name='logoutPage'),
]
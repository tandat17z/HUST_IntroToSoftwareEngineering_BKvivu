from django.urls import path, include
from . import views


app_name = 'settingspage'
urlpatterns = [
    path('', views.settingsPage, name='settingsPage'),
    path('uploadavatar/', views.uploadAvatar, name='uploadAvatar'),
    path('loading', views.changeAvatar, name= "changeAvatar" ),

]
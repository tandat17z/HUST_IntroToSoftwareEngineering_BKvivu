from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'settingspage'
urlpatterns = [
    path('', views.settingsPage, name='settingsPage'),
    path('uploadavatar/', views.uploadAvatar, name='uploadAvatar'),
    path('loading', views.changeAvatar, name= "changeAvatar" ),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)
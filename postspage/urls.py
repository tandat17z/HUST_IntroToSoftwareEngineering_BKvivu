from django.urls import path, include
from . import views

# 3/12
from django.conf import settings
from django.conf.urls.static import static

app_name = 'postspage'
urlpatterns = [
    path('', views.postsPage, name='postsPage'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL) # 3/12

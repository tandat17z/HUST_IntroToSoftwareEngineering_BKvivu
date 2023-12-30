from django.urls import path, include
from . import views

# 3/12
from django.conf import settings
from django.conf.urls.static import static

app_name = 'postspage'
urlpatterns = [
    path('', views.postsPage, name='postsPage'),
    path('posts/', views.postsView, name='posts'),
    path('restaurants/', views.restaurantsView, name='restaurants'),
    path('update_likes/<int:post_id>/', views.update_likes, name='update_likes'),
    path('insert_comment/<int:post_id>/', views.insert_comment, name='insert_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='insert_comment'),
    path('get_comments/<int:post_id>/', views.get_comments, name='get_comments'),
    # path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    # path('test', views.test, name='test')
]   + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL) # 3/12

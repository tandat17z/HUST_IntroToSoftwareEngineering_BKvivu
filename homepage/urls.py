from django.urls import path, include
from . import views

app_name = 'homepage'
urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('login/', views.loginPage, name='loginPage'),
    path('login/register/', views.registerPage, name='registerPage'),
    path('update_likes/<int:post_id>/', views.update_likes, name='update_likes'),

]
from django.urls import path, include
from . import views

app_name = 'profilepage'
urlpatterns = [
    path('<int:acc_id>/', views.profilePage, name='profilePage'),
    path('logout/', views.logout_view, name='logoutPage'),
    path('<int:acc_id>/vote', views.voteProfile, name='voteProfile'),
]
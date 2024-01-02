from django.urls import path, include
from . import views

app_name = 'profilepage'
urlpatterns = [
    path('<int:acc_id>/', views.profilePage, name='profilePage'),
    path('logout/', views.logout_view, name='logoutPage'),
    path('<int:acc_id>/vote', views.voteProfile, name='voteProfile'),
    path('<int:acc_id>/chatDefault', views.chatPageDefault, name='chatDefault'),
    path('<int:acc_id>/chatDefault/chat/<int:user_id>/', views.chatPage, name='chatPage'),
    path('<int:acc_id>/chatDefault/chat/<int:user_id>/save', views.save_message, name='saveMessage'),
    path('<int:acc_id>/chatDefault/chat/<int:user_id>/get', views.get_message, name='getMessage'),
]
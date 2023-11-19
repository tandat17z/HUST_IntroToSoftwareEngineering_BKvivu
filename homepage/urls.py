from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('login', views.login_view),
    path('signup', views.signup_view),
    path('homepage/', views.homepage),
    path('input', views.test),
    path('counter', views.counter),
]

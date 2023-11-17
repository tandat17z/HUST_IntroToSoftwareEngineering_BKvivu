from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('login', views.login_view),
    path('input', views.test),
    path('counter', views.counter),
    
]

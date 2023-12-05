from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import *
from homepage import models

from homepage.models import Post # them mo hinh Post o homepage.models
# from homepage.models import Sharer

# Create your views here.
def postsPage(request):
    posts = Post.objects.filter().order_by('time')
    
    return render(request, 'index.html', {'posts' : posts})
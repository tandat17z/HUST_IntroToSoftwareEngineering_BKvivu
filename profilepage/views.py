from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import *
from homepage.models import *


# Create your views here.
def profilePage(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    
    account = Account.objects.get(user_ptr=request.user)
    context = {
        'account': account,
    }
    return render(request, 'profile.html', context)

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    logout(request)
    return redirect('homepage:homePage')

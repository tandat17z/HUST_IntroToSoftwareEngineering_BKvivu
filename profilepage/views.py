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

    acc = Account.objects.get(user_ptr=request.user)
    if acc.role == "sharer":
        accuser = Sharer.objects.get(account = acc)
    else:
        accuser = Manager.objects.get(account=acc)
    context = {
        'account': acc,
        'accuser': accuser
    }
    return render(request, 'profile.html', context)

# Log out button
def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    logout(request)
    return redirect('homepage:homePage')

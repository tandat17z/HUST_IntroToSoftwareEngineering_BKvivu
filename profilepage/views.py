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
def profilePage(request, acc_id):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    # target_acc , target_user : đối tượng mà mình vào xem trang cá nhân
    target_acc = Account.objects.get(pk=acc_id)
    target_user = Sharer.objects.get(account= target_acc) if target_acc.role == 'sharer' else Manager.objects.get(account= target_acc)
    # acc, user : Bản thân người đang đăng nhập
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    context = {
        'target_user': target_user,
        'user': user,
    }
    return render(request, 'profile.html', context)

# Log out button
def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    logout(request)
    return redirect('homepage:homePage')

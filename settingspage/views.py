from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from homepage.models import *
from .forms import *



# Create your views here.
def settingsPage(request):
    context = {

    }
    return render(request, 'settings.html', context)

# Upload avatar
def uploadAvatar(request):
    uAvatar = UploadAvatar()
    return render(request, 'uploadAvatar.html', {'form': uAvatar});


def changeAvatar(request):
    # Kiểm tra trạng thái đăng nhập
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    # Đã đăng nhập, xử lý upload ảnh
    account = Account.objects.get(user_ptr=request.user)
    if(request.method == "POST"):
        form = UploadAvatar(request.POST, request.FILES, instance=account)
        if form.is_valid():
            # Thực hiện thay đổi avatar
            newA  =form.save(commit=False)
            newA.save()
            # newA.avatar: Avatar mới
            #Trả về trang cá nhân
            return redirect('profilepage:profilePage')
        else:
            return HttpResponse("Ảnh không hợp lệ")
    else:
        return HttpResponse("không phải post ")
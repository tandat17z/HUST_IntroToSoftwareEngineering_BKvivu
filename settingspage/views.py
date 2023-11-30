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
    return render(request, 'settings.html')

def postPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    if request.method == 'POST':
        post = Post.objects.create(account = acc)
        img = Image.objects.create(post = post)
        form_post= CreatePostForm(request.POST, request.FILES, instance=post)
        form_img = CreateImgForm(request.POST, request.FILES, instance=img)
        if form_post.is_valid() and form_img.is_valid() :
            # Thực hiện thay đổi avatar
            _post  = form_post.save(commit=False)
            _post.save()

            _img  = form_img.save(commit=False)
            _img.save()
            # newA.avatar: Avatar mới
            #Trả về trang cá nhân
            messages.success(request, 'Tạo bài viết thành công')
        else:
            messages.error(request, 'Thất bại')

    form_post = CreatePostForm()
    form_img = CreateImgForm()
    context = {
        'form_post': form_post,
        'form_img': form_img,
    }
    return render(request, 'post.html', context)

def generalPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)

    if request.method == 'POST':
        if acc.role == 'sharer':
            form = UpdateSharerForm(request.POST, request.FILES, instance=user)
        else:
            form = UpdateManagerForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Thực hiện thay đổi avatar
            newA  =form.save(commit=False)
            newA.save()
            # newA.avatar: Avatar mới
            #Trả về trang cá nhân
            messages.success(request, 'Thông tin đã được cập nhật')

    form_general = UpdateSharerForm() if acc.role == 'sharer' else UpdateManagerForm()

    context = {
        'form_gerenal': form_general,
    }
    return render(request, 'general.html', context)
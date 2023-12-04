from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.
def homePage(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)

    top_shops = Manager.objects.filter(rank__isnull=False).order_by('-rank')[:5]
    list_items = Product.objects.order_by('-time')[:15]
    context = {
        'acc': acc,
        'user': user,
        'top_shops': top_shops,
        'list_items': list_items,
    }
    return render(request, 'homepage.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('homepage:homePage')
    
    if request.method == 'POST':
        rgt_username = request.POST.get('rgt_username')
        username = request.POST.get('username')

        if rgt_username:  #nếu đăng kí (register)
            email =  request.POST.get('rgt_email')
            password1 =  request.POST.get('rgt_psw')
            password2 =  request.POST.get('rgt_repsw')
            role = request.POST.get('role')
            data = {
                'username': rgt_username,
                'password1': password1,
                'password2': password2,
            }
            form = UserCreationForm(data)
            if form.is_valid and password1 == password2:
                # form.save()
                psw = password1
                hashed_psw = make_password(psw)
                acc = Account.objects.create(
                    username=rgt_username, 
                    email=email, 
                    password=hashed_psw, 
                    raw_password=psw, 
                    role=role
                )
                
                #Tạo model(Sharer/ Manager) tương ứng
                if acc:
                    user_logged = authenticate(request, username=rgt_username, password=psw)
                    login(request, user_logged)
                    return redirect('homepage:registerPage')
            messages.error(request, 'Đăng kí không thành công. Vui lòng thử lại.')
        elif username:
            psw = request.POST.get('password')
            user_logged = authenticate(request, username=username, password=psw)
            if user_logged is not None:
                login(request, user_logged)
                return redirect('homepage:homePage')
            messages.error(request, 'Đăng nhập không thành công. Vui lòng thử lại.')
    
    context = {
        'form_rgt': CreateAccountForm(),
    }
    # messages.error(request, 'Đăng nhập')
    return render(request, 'login.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        acc = Account.objects.get(username=request.user.username)
        if acc.role == "sharer" :
            if request.method == "POST":
                name = request.POST.get('name')
                sharer = Sharer.objects.create(account = acc, name = name)
                form = CreateSharerForm(request.POST, instance=sharer)
                if form.is_valid():
                    # Thực hiện thay đổi avatar
                    sharer = form.save(commit=False)
                    sharer.save()
                
                    return redirect('homepage:homePage')
            context = {
                'form' :  CreateSharerForm(),
            }
        else:
            if request.method=="POST":
                name = request.POST.get('name')
                address = request.POST.get('address')
                manager = Manager.objects.create(account = acc, name = name, address=address)
                form = CreateManagerForm(request.POST, instance=manager)
                if form.is_valid():
                    # Thực hiện thay đổi avatar
                    manager = form.save(commit=False)
                    manager.save()
                    return redirect('homepage:homePage')
            context = {
                'form' :  CreateManagerForm(),
            }

    return render(request, 'register.html', context)
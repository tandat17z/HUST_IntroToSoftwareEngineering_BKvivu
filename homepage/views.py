from django.shortcuts import render, redirect
from django.http import HttpResponse

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
    context = {
        'account': Account.objects.get(user_ptr=request.user),
    }
    return render(request, 'homepage.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('homepage:homePage')
    if request.method == 'POST':
        rgt_username = request.POST.get('rgt_username')
        username = request.POST.get('username')

        if rgt_username:  #nếu đăng kí (register)
            password1 =  request.POST.get('rgt_psw')
            password2 =  request.POST.get('rgt_repsw')
            role = request.POST.get('role')
            name = request.POST.get('name')
            data = {
                'username': rgt_username,
                'password1': password1, 
                'password2': password2,
            }
            form = UserCreationForm(data)
            if form.is_valid:
                # form.save()
                psw = password1
                hashed_psw = make_password(psw)
                acc = Account.objects.create(username=rgt_username, password=hashed_psw, raw_password=psw, role=role)
                #Tạo model(Sharer/ Manager) tương ứng
                if role == 'Sharer':
                    sharer = Sharer.objects.create(account=acc, name=name)
                else:
                    manager = Manager.objects.create(account=acc, name=name)
                    
                user_logged = authenticate(request, username=rgt_username, password=psw)
                login(request, user_logged)
                return redirect('homepage:homePage')
            
        elif username:
            psw = request.POST.get('password')
            user_logged = authenticate(request, username=username, password=psw)
            if user_logged is not None:
                login(request, user_logged)
                return redirect('homepage:homePage')
            
    context = {
        'form_rgt': CreateAccountForm(),
    }
    return render(request, 'login.html', context)
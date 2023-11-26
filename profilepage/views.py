from django.shortcuts import render, redirect
from django.contrib.auth import logout
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

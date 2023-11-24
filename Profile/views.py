from django.shortcuts import render
from Homepage1.models import *
# Create your views here.
def profile(request, username):
    tks = TaiKhoan.objects.filter(username = username)
    context = {
        'tk': tks[0],
        'username': username,
    }
    return render(request, 'profile/profile.html', context)
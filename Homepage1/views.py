from django.shortcuts import render,redirect, reverse
from django.http import HttpResponse
from django.template import loader
from .models import *


# global user
# Create your views here.
def home(request, username):
  # template = loader.get_template('home/main.html')
  # return HttpResponse(template.render())
  tks = TaiKhoan.objects.filter(username = username)
  context = {
    'tk': tks[0]
  }
  return render(request, 'home/homepage.html', context)

def login(request):
  if request.method == 'POST':
    su_name = request.POST.get('su-username')
    login_name = request.POST.get('username')
    if su_name:
      # đăng kí
      username = su_name
      psw = request.POST.get('su-psw')
      psw_repeat = request.POST.get('su-psw-repeat')
      tks = TaiKhoan.objects.filter(username = username)
      if len(tks) == 0 and psw == psw_repeat:
        tk = TaiKhoan(username=username, password= psw, vaitro = 'u')
        tk.save()
        redirect_url = reverse('home', args=[username])
        return redirect(redirect_url)
    else:
      username = login_name
      psw = request.POST.get('password')
      tks = TaiKhoan.objects.filter(username = username)
      if len(tks) == 1 and tks[0].password == psw:
        tk = tks[0]
        context = {
          'taikhoan': tk,
        }
        redirect_url = reverse('home', args=[username])
        return redirect(redirect_url)
  return render(request, 'home/login.html')
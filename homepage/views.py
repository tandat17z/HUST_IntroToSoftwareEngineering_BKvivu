from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

# Create your views here.
def main(request):
  # template = loader.get_template('home/main.html')
  # return HttpResponse(template.render())
  return render(request, 'home/notLogin.html')

def signup_view(request):
  username = request.POST['su-username']
  psw = request.POST['su-psw']
  psw_repeat = request.POST['su-psw-repeat']

  user = User.objects.filter(username = username)
  if psw != psw_repeat or len(user) > 0:
    signup = False
  else:
    signup = True
    new_user = User(username= username, password = psw)
    new_user.save()

  context = {
    'signup': signup,
    'login': True,
    'username': username,
  }
  return render(request, 'home/alert.html', context)


def homepage(request):
  return render(request, 'home/homepage.html')

def login_view(request):
  username = request.POST['username']
  password = request.POST['password']

  user = User.objects.filter(username = username)
  if len(user) != 1:
    print('Lỗi trùng tên đăng nhập')
    logged = False
  elif user[0].password == password:
    logged = True
  else:
    logged = False

  context = {
    'type': False,
    'signup': False,
    'login': logged,
    'username': username,
  }
  return render(request, 'home/alert.html', context)


def test(request):
  return render(request, 'home/index.html')

def counter(request):
  words = request.POST['text']
  n = len(words.split())
  return render(request, 'home/counter.html', {'n': n})
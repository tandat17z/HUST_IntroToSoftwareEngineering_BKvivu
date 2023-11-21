from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *


# global user
# Create your views here.
def main(request):
  # template = loader.get_template('home/main.html')
  # return HttpResponse(template.render())
  return render(request, 'home/notLogin.html')

def signup_view(request):
  username = request.POST['su-username']
  psw = request.POST['su-psw']
  psw_repeat = request.POST['su-psw-repeat']

  users = User.objects.filter(username = username)
  if psw != psw_repeat or len(users) > 0:
    signup = False
    context = {
      'signup': signup,
      'login': True,
    }
  else:
    signup = True
    new_user = User(username= username, password = psw)
    new_user.save()
    global user
    user = new_user
    context = {
      'signup': signup,
      'login': True,
      'username': user.username,
    }
  return render(request, 'home/alert.html', context)


def homepage(request):
  print(user)
  context ={
    'user': user,
  }
  return render(request, 'home/homepage.html', context)

def login_view(request):
  username = request.POST['username']
  password = request.POST['password']

  users = User.objects.filter(username = username)
  if len(users) != 1:
    print('Lỗi trùng tên đăng nhập')
    logged = False
  elif users[0].password == password:
    logged = True
    global user
    user = users[0]
  else:
    logged = False

  if logged:
    context = {
      'type': False,
      'signup': False,
      'login': logged,
      'username': user.username,
    }
  else:
    context = {
      'type': False,
      'signup': False,
      'login': logged,
      # 'username': user.username,
    }
  return render(request, 'home/alert.html', context)


# def test(request):
#   return render(request, 'home/index.html')

# def counter(request):
#   words = request.POST['text']
#   n = len(words.split())
#   return render(request, 'home/counter.html', {'n': n})

def testtruong(request, username):
  context = {
    'username': username,
  }
  return render(request, 'profile/profile.html', context)
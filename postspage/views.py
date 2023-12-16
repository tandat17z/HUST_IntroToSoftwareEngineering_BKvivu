from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import *
from homepage import models

from homepage.models import Post # them mo hinh Post o homepage.models
# from homepage.models import Sharer
from homepage.models import Manager


from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Tăng số lượt thích của bài viết
    post.like += 1
    post.save()

    # Trả về dữ liệu dưới dạng JSON
    data = {'like_count': post.like}
    return JsonResponse(data)



# Create your views here.
def postsPage(request):
    posts = Post.objects.filter().order_by('time')
    managers = Manager.objects.filter().order_by('-avgStar')
    
    return render(request, 'index.html', {'posts' : posts, 'managers' : managers})
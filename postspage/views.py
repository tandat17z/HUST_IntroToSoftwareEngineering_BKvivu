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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def like_post(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(pk=post_id)
    user_like, created = UserLike.objects.get_or_create(user=request.user, post=post)

    if not created:
        if user_like.value == 1:
            user_like.value = -1
        else:
            user_like.value = 1
        user_like.save()

    like_count = UserLike.objects.filter(post=post).aggregate(Sum('value'))

    return JsonResponse({'like_count': like_count})

# def like_post(request, post_id):
#     post = get_object_or_404(Post, id=post_id)

#     # Tăng số lượt thích của bài viết
#     post.like += 1
#     post.save()

#     # Trả về dữ liệu dưới dạng JSON
#     data = {'like_count': post.like}
#     return JsonResponse(data)



# Create your views here.
def postsPage(request):
    posts = Post.objects.filter().order_by('time')
    managers = Manager.objects.filter().order_by('-avgStar')
    
    return render(request, 'index.html', {'posts' : posts, 'managers' : managers})
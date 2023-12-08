from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import *
from homepage.models import *


# Create your views here.
def profilePage(request, acc_id):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    # target_acc , target_user : đối tượng mà mình vào xem trang cá nhân
    target_acc = Account.objects.get(pk=acc_id)
    target_user = Sharer.objects.get(account= target_acc) if target_acc.role == 'sharer' else Manager.objects.get(account= target_acc)
    # acc, user : Bản thân người đang đăng nhập
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    # Lấy số sao đã vote của người đăng nhập nếu profile đang xem là Manager
    starsvotetarget = 5
    if(target_acc.role == 'manager') and (target_acc.id != acc.id):
        try:
            voteobj = StarVote.objects.get(account=acc, manager= target_user)
            starsvotetarget = voteobj.stars
        except:
            pass
    context = {
        'target_user': target_user,
        'user': user,
        'starsvotetarget': starsvotetarget
    }
    return render(request, 'profile.html', context)

#vote Profile manager
def voteProfile(request,acc_id):
    if request.method == 'POST':
        try:
            acc = Account.objects.get(user_ptr=request.user)
            target_user=Manager.objects.get(account= acc_id)
            stars = request.POST.get("rate")
            # Lấy hoặc tạo một đối tượng StarVote dựa trên account_id và manager_id
            star_vote, created = StarVote.objects.get_or_create(
                account = acc,
                manager = target_user,
                defaults={'stars': stars}  # Điền vào giá trị mặc định cho số sao nếu đối tượng chưa tồn tại
            )
            if not created:
            # Đối tượng đã tồn tại, bạn có thể thực hiện các thay đổi tùy thuộc vào trường hợp của bạn
                star_vote.stars = stars
                star_vote.save()
            target_user.save() #Cập nhật rank cho người quản lý
        except:
            pass
    else:
        pass
    return redirect('profilepage:profilePage', acc_id=acc_id)

# Log out button
def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')
    logout(request)
    return redirect('homepage:homePage')

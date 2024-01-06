from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
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



#Chat
def chatPageDefault(request, acc_id):
    if request.method == 'GET': 
        acc1 = Account.objects.get(user_ptr=request.user)
        user1 = Sharer.objects.get(account= acc1) if acc1.role == 'sharer' else Manager.objects.get(account= acc1)
        
        all_user = Message.objects.filter(
        models.Q(sender=acc1) | models.Q(receiver=acc1)).values('receiver').exclude(receiver=acc1.id).distinct() if acc1.role == 'manager' else Message.objects.filter(
        models.Q(sender=acc1) | models.Q(receiver=acc1)).values('sender').exclude(sender=acc1.id).distinct()
         
        #default : tuong tac 2 chieu roi, i send you , you send me
        list_all_user = []
        for user in all_user:
            add_user = Manager.objects.get(pk=user['sender']) if acc1.role == 'sharer' else Sharer.objects.get(pk=user['receiver'])
            list_all_user.append(add_user)

        context = {
            'acc_id': acc_id,
            'user1' : user1,
            'all_user': list_all_user
        }
        return render(request, "chat/chat_base.html", context)
    
def chatPage(request, acc_id, user_id):
    if request.method == 'GET': 
        acc1 = Account.objects.get(user_ptr=request.user)
        acc2 = Account.objects.get(id = user_id)
        user1 = Sharer.objects.get(account= acc1) if acc1.role == 'sharer' else Manager.objects.get(account= acc1)
        user2 = Sharer.objects.get(account= acc2) if acc2.role == 'sharer' else Manager.objects.get(account= acc2)
        # check if user2 has conversation with user1, if not initialize it 
        all_user_filter = Message.objects.filter(
        models.Q(sender=acc1) | models.Q(receiver=acc1)).values('receiver').exclude(receiver=acc1.id).distinct() if acc1.role == 'manager' else Message.objects.filter(
        models.Q(sender=acc1) | models.Q(receiver=acc1)).values('sender').exclude(sender=acc1.id).distinct()
        has = False
        if acc1.role == 'sharer':
            for user in all_user_filter:
                if user['sender'] == user_id : 
                    has = True
            if not has: 
                Message.objects.create(content="Xin chào bạn, bạn đang quan tâm đến sản phẩm nào của chúng mình ạ.", sender=acc2, receiver=acc1, time=timezone.datetime.now())
        
        message = Message.objects.filter(
            (models.Q(receiver=acc1) & models.Q(sender=acc2)) | 
            (models.Q(receiver=acc2) & models.Q(sender=acc1))).order_by('time')
        
        all_user = Message.objects.filter(
        models.Q(sender=acc1) | models.Q(receiver=acc1)).values('receiver').exclude(receiver=acc1.id).distinct() if acc1.role == 'manager' else Message.objects.filter(
        models.Q(sender=acc1) | models.Q(receiver=acc1)).values('sender').exclude(sender=acc1.id).distinct()
        
  
        list_all_user = []
        for user in all_user:
            add_user = Manager.objects.get(pk=user['sender']) if acc1.role == 'sharer' else Sharer.objects.get(pk=user['receiver'])
            list_all_user.append(add_user)

        context = {
            'acc_id': acc_id,
            'user_id': user_id,
            'user1' : user1,
            'user2' : user2,
            'message' : message, 
            'all_user': list_all_user
        }
        return render(request, "chat/chat.html", context)
#send message
def save_message(request, acc_id, user_id):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        acc1 = Account.objects.get(user_ptr=request.user)
        acc2 = Account.objects.get(id = user_id)
        user1 = Sharer.objects.get(account= acc1) if acc1.role == 'sharer' else Manager.objects.get(account= acc1)
        user2 = Sharer.objects.get(account= acc2) if acc2.role == 'sharer' else Manager.objects.get(account= acc2)
        newMessage = Message.objects.create(sender=acc1, receiver=acc2, content=request.POST.get('content'), time=timezone.datetime.now()),
        message_id = newMessage[0].id
        time = newMessage[0].time
        data = {'message': content, 'time': time, 'success' : True, 'user_id': user_id, 'message_id': message_id}
        return JsonResponse(data)
#update message
def get_message(request, acc_id, user_id):
    acc1 = Account.objects.get(user_ptr=request.user)
    acc2 = Account.objects.get(id = user_id)
    user1 = Sharer.objects.get(account= acc1) if acc1.role == 'sharer' else Manager.objects.get(account= acc1)
    user2 = Sharer.objects.get(account= acc2) if acc2.role == 'sharer' else Manager.objects.get(account= acc2)
    messages = Message.objects.filter(
            (models.Q(receiver=acc1) & models.Q(sender=acc2)) | 
            (models.Q(receiver=acc2) & models.Q(sender=acc1))).order_by('time')
    message_list = list(messages.values())
    user1_dic = {
        'account_id': user1.account_id,
    }
    user2_dic = {
        'account_id': user2.account_id,
    }
    data = {
        'messages': message_list,
        'success': True,
        'user1': user1_dic,
        'user2': user2_dic,
    } 
    return JsonResponse(data)

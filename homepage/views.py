from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from unidecode import unidecode
from django.db.models import Q

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import *
from .forms import *

from func.func import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def searchTag__(type): # Tìm kiếm theo tag -> list product
    searchShop = []
    # Tên có chưa tag hoặc type = tag
    searchProduct = Product.objects.filter(Q(name_stripped__icontains=type) | Q(type__icontains=type))
    return searchShop, searchProduct

@csrf_exempt
def searchTag(request, tag):
    tag = tag.replace("_", " ")
    searchShop = []
    searchProduct = []

    searchProduct = Product.objects.filter(Q(name_stripped__icontains=tag) | Q(type__icontains=tag)).order_by('price')
    if request.method == 'POST':
        choices = request.POST.get('choices')
        if choices == 'shop':
            for shop in  Manager.objects.filter(name_stripped__icontains=tag):
                searchShop.append(shop)
            for product in searchProduct:
                if product.provider not in searchShop:
                    searchShop.append(product.provider)
            searchShop = sorted(searchShop, key=lambda obj: -obj.avgStar)
            dataShop = getDataShop(searchShop)
            return JsonResponse({'dataShop': dataShop})
        
        elif choices == 'product':
            dataProduct = getDataProduct(searchProduct)
            return JsonResponse({'dataProduct': dataProduct})

@csrf_exempt 
def mainSearch(request):
    if request.method == 'POST':
        type = request.POST.get('choices')
        searchKey = request.POST.get('searchKey')
        words = unidecode(searchKey.lower()).split()
        searchKey = ' '.join(words)
        city, district, ward = getArea(
            request.POST.get('city'),
            request.POST.get('district'),
            request.POST.get('ward')
        )
        
        t_open = request.POST.get('t_open')
        t_closed = request.POST.get('t_closed')
        if type == 'shop':
            searchShop = searchAndFilter(searchKey, type='shop',
                                       area={
                                           'ward': ward,
                                           'district': district,
                                           'city': city
                                       },
                                       open=t_open, closed=t_closed)
            dataShop = getDataShop(searchShop)
            return JsonResponse({'dataShop': dataShop})
        else:
            searchProduct = searchAndFilter(searchKey, type='product',
                                       area={
                                           'ward': ward,
                                           'district': district,
                                           'city': city
                                       },
                                       open=t_open, closed=t_closed)
            dataProduct = getDataProduct(searchProduct)
            print(dataProduct)
            return JsonResponse({'dataProduct': dataProduct})


def getDataShop(searchShop):
    dataShop = list()
    for item in searchShop:
        print(item.account.id)
        dataShop.append( {
            'id': item.account.id,
            'avatar': item.avatar.url,
            'name': item.name,
            'avgStar': item.avgStar,
            'district': item.district,
            'ward': item.ward
        })
    return dataShop

def getDataProduct(searchProduct):
    dataProduct = list()
    for product in searchProduct:
        dataProduct.append({
            'id': product.id,
            'name': product.name,
            'provider': {
                'id': product.provider.account.id,
                'name': product.provider.name,
                'avatar': product.provider.avatar.url,
            },
            'img': product.img.url,
            'price': product.price
        })
    return dataProduct


def searchAndFilter(keyword = '', 
                    type='product', 
                    area={'ward': 'all', 'district': 'all', 'city': 'all'}, 
                    open="00:00", closed="23:59"):
    '''
    Tìm các shop hợp lệ, tìm sản phẩm của shop đó (dk thoi gian + vitri)
    '''
    # if open <= closed: # tìm bình thường
    searchShop = Manager.objects.filter(
        Q(t_open__gte=open, t_open__lte=closed ) 
        | Q(t_closed__gte=open, t_closed__lte=closed ) 
        | Q(t_open__lte=open, t_closed__gte=closed)
    )
    

    if area['ward'] != 'all': searchShop = searchShop.filter(ward=area['ward'])
    elif area['district'] != 'all': searchShop = searchShop.filter(district=area['district'])
    elif area['city'] != 'all': searchShop = searchShop.filter(city=area['city'])

    searchProduct = Product.objects.filter(provider__in=searchShop)
    listShop = searchShop
    print(listShop)
    # Tìm với từ khóa
    if keyword != '':
        listShop = list()
        searchProduct = searchProduct.filter(name_stripped__icontains=keyword).order_by('-time')

        for shop in  searchShop.filter(name_stripped__icontains=keyword).order_by('-avgStar'):
            listShop.append(shop)

        for product in searchProduct:
            if product.provider not in listShop:
                listShop.append(product.provider)
        listShop = sorted(listShop, key=lambda obj: -obj.avgStar)
        print(listShop)
    if type == 'shop':
        return listShop
    else:
        return searchProduct

# Create your views here.
def homePage(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')

    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)

    # list top cửa hàng-------------- 
    top_shops = Manager.objects.filter(avgStar__isnull=False).order_by('-avgStar')[:5]
    # list top posts-------------
    posts = Post.objects.filter().order_by('-like')[:5]

    info = list()
    for p in posts:
        author = Sharer.objects.get(account= p.account) if p.account.role == 'sharer' else Manager.objects.get(account= p.account)
        try:
            userLike = UserLike.objects.get(account=acc, post=p) 
        except:
            userLike = None
        info.append({
            'post': p, 
            'author': author, 
            'userLike': userLike,
            'img': Image.objects.filter(post = p)
        })

    # Mặc định chưa tìm kiếm là hiển thị các sản phẩm mới nhất
    searchProduct = Product.objects.order_by('-time')

    context = {
        'acc': acc,
        'user': user,
        'top_shops': top_shops,
        'topPosts': info,
        'searchProduct': searchProduct,
    }
    return render(request, 'homepage.html', context)

def loginPage(request):
    '''
    Trang ban đầu vào web: chọn login + register
    '''
    if request.user.is_authenticated:
        return redirect('homepage:homePage')

    messAlert = list()
    if request.method == 'POST':
        if 'register' in request.POST:  #nếu đăng kí (register)
            rgt_username = request.POST.get('rgt_username')
            email =  request.POST.get('rgt_email')
            password1 =  request.POST.get('rgt_psw')
            password2 =  request.POST.get('rgt_repsw')
            role = request.POST.get('role')
            data = {
                'username': rgt_username,
                'password1': password1,
                'password2': password2,
            }
            form = UserCreationForm(data)
            if form.is_valid:
                #form.save() # tích hợp tạo user trong Account r
                psw = password1
                hashed_psw = make_password(psw)
                try:
                    acc = Account.objects.create(
                        username=rgt_username,
                        email=email,
                        password=hashed_psw,
                        raw_password=psw,
                        role=role
                    )
                except:
                    acc = None
                    print("Tạo acc không thành công")
                    pass
                if acc:
                    print("Tạo acc thành công")
                    #Tạo model(Sharer/ Manager) tương ứng
                    if role == 'manager':
                        manager = Manager.objects.create(
                            account = acc,
                            name = rgt_username
                        )
                    elif role == 'sharer':
                        sharer = Sharer.objects.create(
                            account = acc, 
                            name = rgt_username
                        )
                    user_logged = authenticate(request, username=rgt_username, password=psw)
                    login(request, user_logged)
                    return redirect('homepage:registerPage')
            messAlert.append('Đăng kí không thành công. Vui lòng thử lại.') 
        elif 'login' in request.POST:
            username = request.POST.get('username')
            psw = request.POST.get('password')
            user_logged = authenticate(request, username=username, password=psw)
            if user_logged is not None:
                login(request, user_logged)
                messages.success(request, 'Đăng nhập thành công rùi nhé.')
                return redirect('homepage:homePage')
            messAlert.append('Đăng nhập không thành công. Vui lòng thử lại.')

    # messages.error(request, 'Đăng nhập')
    return render(request, 'login.html', {'messAlert': messAlert})

def registerPage(request):
    if request.user.is_authenticated:
        acc = Account.objects.get(username=request.user.username)
        if acc.role == "sharer" :
            if request.method == "POST":
                sharer = Sharer.objects.get(
                    account = acc
                )
                sharer.name = request.POST.get('name')
                sharer.age = request.POST.get('age')

                city_id = request.POST.get('city')
                district_id = request.POST.get('district')
                ward_id = request.POST.get('ward')

                # print((city_id, district_id, ward_id))
                sharer.city, sharer.district, sharer.ward = getArea(city_id, district_id, ward_id)
                # print((city, district, ward))

                sharer.bio = request.POST.get('comment')
                sharer.save()
                return redirect('homepage:homePage')
        else:
            if request.method=="POST":
                manager = Manager.objects.get(account = acc)
                manager.name = request.POST.get('name')
                manager.phone = request.POST.get('phone')

                city_id = request.POST.get('city')
                district_id = request.POST.get('district')
                ward_id = request.POST.get('ward')

                manager.address = request.POST.get('address')
                manager.city, manager.district, manager.ward = getArea(city_id, district_id, ward_id)
                
                manager.bio = request.POST.get('comment')
                manager.save()
                return redirect('homepage:homePage')
        context = {
            'role' :  acc.role,
        }
        return render(request, 'register.html', context)

@csrf_exempt
def update_likes(request, post_id):
    acc = Account.objects.get(user_ptr=request.user)
    post = Post.objects.get(id = post_id)
    if request.method == 'POST':
        # Nhận dữ liệu từ yêu cầu AJAX
        data = json.loads(request.body)
        if( post.like < data['like'] ):
            userLike = UserLike.objects.create(
                account = acc,
                post = post
            )
        else:
            userLike = UserLike.objects.get(
                account = acc,
                post = post
            )
            userLike.delete()
        post.like = data['like']
        post.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
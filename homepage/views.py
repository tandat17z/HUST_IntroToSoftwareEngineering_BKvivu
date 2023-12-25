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

def searchTag(type):
    searchShop = Manager.objects.filter(name_stripped__icontains=type)
    searchProduct = Product.objects.filter(Q(name_stripped__icontains=type) | Q(type__icontains=type))
    return searchShop, searchProduct

def searchAndFilter(keyword, area='all', open="00:00", closed="23:59"):
    shopOpen = Manager.objects.filter(Q(t_open__gte=open, t_open__lte=closed ) | Q(t_closed__gte=open, t_closed__lte=closed))
    searchShop = shopOpen.filter(name_stripped__icontains=keyword)
    searchProduct = Product.objects.filter(name_stripped__icontains=keyword, provider__in=shopOpen)

    if area != 'all':
        searchShop = searchShop.filter(ward=area)
        searchProduct = searchProduct.filter(provider__in=searchShop)
    
    return searchShop, searchProduct


# Create your views here.
def homePage(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')

    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)

    # list top cửa hàng 
    top_shops = Manager.objects.filter(avgStar__isnull=False).order_by('-avgStar')[:5]

    if request.method == 'POST': # Ở trang thái tìm kiếm sản phẩm, lọc
        if 'bundau' in request.POST:
            searchShop, searchProduct = searchTag('bun dau')
        elif 'comrang' in request.POST:
            searchShop, searchProduct = searchTag('com rang')
        elif 'nemnuong' in request.POST:
            searchShop, searchProduct = searchTag('nem nuong')
        elif 'congvien' in request.POST:
            searchShop, searchProduct = searchTag('cong vien')
        elif 'baotang' in request.POST:
            searchShop, searchProduct = searchTag('bao tang')
        else:
            keyword = request.POST.get('search')
            keyword_stripped = unidecode(keyword)
            city, district, area = getArea(
                request.POST.get('city'),
                request.POST.get('district'),
                request.POST.get('ward')
            )
            open = request.POST.get("t_open")
            closed = request.POST.get("t_closed")
            print(keyword, "--", area, open, closed)
            searchShop, searchProduct = searchAndFilter(keyword_stripped, area, open, closed)
    else: # Mặc định trả ra list sản phẩm mới nhất
        searchShop = []
        searchProduct = Product.objects.order_by('-time')[:15]

    context = {
        'acc': acc,
        'user': user,
        'top_shops': top_shops,
        'searchShop': searchShop,
        'searchProduct': searchProduct,
    }
    return render(request, 'homepage.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('homepage:homePage')

    if request.method == 'POST':
        rgt_username = request.POST.get('rgt_username')
        username = request.POST.get('username')

        if rgt_username:  #nếu đăng kí (register)
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
            if form.is_valid and password1 == password2:
                # form.save()
                psw = password1
                hashed_psw = make_password(psw)
                acc = Account.objects.create(
                    username=rgt_username,
                    email=email,
                    password=hashed_psw,
                    raw_password=psw,
                    role=role
                )

                #Tạo model(Sharer/ Manager) tương ứng
                if acc:
                    user_logged = authenticate(request, username=rgt_username, password=psw)
                    login(request, user_logged)
                    return redirect('homepage:registerPage')
            messages.error(request, 'Đăng kí không thành công. Vui lòng thử lại.')
        elif username:
            psw = request.POST.get('password')
            user_logged = authenticate(request, username=username, password=psw)
            if user_logged is not None:
                login(request, user_logged)
                return redirect('homepage:homePage')
            messages.error(request, 'Đăng nhập không thành công. Vui lòng thử lại.')

    context = {
        'form_rgt': CreateAccountForm(),
    }
    # messages.error(request, 'Đăng nhập')
    return render(request, 'login.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        acc = Account.objects.get(username=request.user.username)
        if acc.role == "sharer" :
            if request.method == "POST":
                name = request.POST.get('name')
                age = request.POST.get('age')

                city_id = request.POST.get('city')
                district_id = request.POST.get('district')
                ward_id = request.POST.get('ward')

                print((city_id, district_id, ward_id))
                city, district, ward = getArea(city_id, district_id, ward_id)
                print((city, district, ward))

                bio = request.POST.get('comment')
                sharer = Sharer.objects.create(
                    account = acc, 
                    name = name,
                    city = city, district = district, ward = ward,
                    age = age,
                    bio = bio
                )
                return redirect('homepage:homePage')
        else:
            if request.method=="POST":
                name = request.POST.get('name')
                phone = request.POST.get('phone')

                city_id = request.POST.get('city')
                district_id = request.POST.get('district')
                ward_id = request.POST.get('ward')
                address = request.POST.get('address')
                city, district, ward = getArea(city_id, district_id, ward_id)
                
                bio = request.POST.get('comment')
                manager = Manager.objects.create(
                    account = acc, 
                    name = name, 
                    phone = phone,
                    city = city, district = district, ward = ward,
                    address=address,
                    bio = bio)
                return redirect('homepage:homePage')
        context = {
            'role' :  acc.role,
        }
        return render(request, 'register.html', context)

def test(request):
    return render(request, 'manager.html')
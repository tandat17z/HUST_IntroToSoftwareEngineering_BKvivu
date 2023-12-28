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

def searchTag(type): # Tìm kiếm theo tag -> list product
    searchShop = []
    # Tên có chưa tag hoặc type = tag
    searchProduct = Product.objects.filter(Q(name_stripped__icontains=type) | Q(type__icontains=type))
    return searchShop, searchProduct

def searchAndFilter(keyword = '', 
                    type='product', 
                    area={'ward': 'all', 'district': 'all', 'city': 'all'}, 
                    open="00:00", closed="23:59"):
    '''
    Tìm các shop hợp lệ, tìm sản phẩm của shop đó
    '''
    searchShop = []
    searchProduct = []
    
    # print("in", keyword, type, area, open, closed)
    #Những shop đang mở cửa và ở trong khu vực tìm kiếm
    searchShop = Manager.objects.filter(Q(t_open__gte=open, t_open__lte=closed ) | Q(t_closed__gte=open, t_closed__lte=closed ))
    if area['ward'] != 'all': searchShop = searchShop.filter(ward=area['ward'])
    elif area['district'] != 'all': searchShop = searchShop.filter(district=area['district'])
    elif area['city'] != 'all': searchShop = searchShop.filter(city=area['city'])
    searchProduct = Product.objects.filter(provider__in=searchShop)
    print(area)
    print(searchShop)
    print(searchProduct)
    # Tìm với từ khóa
    if keyword != '':
        searchShop = searchShop.filter(name_stripped__icontains=keyword)
        searchProduct = searchProduct.filter(name_stripped__icontains=keyword)

    print(searchShop)
    print(searchProduct)
    if type == 'shop':
        return searchShop.order_by('-avgStar'), []
    else:
        return [], searchProduct.order_by('-time')

# Create your views here.
def homePage(request):
    if not request.user.is_authenticated:
        return redirect('homepage:loginPage')

    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)

    # list top cửa hàng 
    top_shops = Manager.objects.filter(avgStar__isnull=False).order_by('-avgStar')[:5]
    print("load Homepage --------------")
    if request.method == 'POST': # Ở trang thái tìm kiếm sản phẩm, lọc
        # Tìm kiếm ở header
        if 'headerSearch' in request.POST:
            keyword = request.POST.get('search')
            keyword_stripped = unidecode(keyword).strip() # Tìm kiếm không dấu
            print("vào phần searchHeader")
            searchShop, searchProduct = searchAndFilter(keyword_stripped)
        # Tìm kiếm theo tag ------------------
        elif 'bundau' in request.POST:
            searchShop, searchProduct = searchTag('bun dau')
        elif 'comrang' in request.POST:
            searchShop, searchProduct = searchTag('com rang')
        elif 'nemnuong' in request.POST:
            searchShop, searchProduct = searchTag('nem nuong')
        elif 'congvien' in request.POST:
            searchShop, searchProduct = searchTag('cong vien')
        elif 'baotang' in request.POST:
            searchShop, searchProduct = searchTag('bao tang')
        # Tìm kiếm chuẩn --------------------
        elif 'search' in request.POST:
            keyword = request.POST.get('search')
            keyword_stripped = unidecode(keyword).strip() # Tìm kiếm không dấu
            type = request.POST.get('type')
            city, district, ward = getArea(
                request.POST.get('city'),
                request.POST.get('district'),
                request.POST.get('ward')
            )
            area = {
                'ward': ward, 
                'district': district, 
                'city': city
            }
            open = request.POST.get("t_open")
            closed = request.POST.get("t_closed")
            print("vào phần tìm kiếm rồi")
            # print(type, area, open, closed, keyword_stripped)
            searchShop, searchProduct = searchAndFilter(keyword_stripped, type, area, open, closed)
    
    else: # Mặc định trả ra list sản phẩm mới nhất
        searchShop = []
        searchProduct = Product.objects.order_by('-like')

    context = {
        'acc': acc,
        'user': user,
        'top_shops': top_shops,
        'searchShop': searchShop,
        'searchProduct': searchProduct,
    }
    return render(request, 'homepage.html', context)

def loginPage(request):
    '''
    Trang ban đầu vào web: chọn login + register
    '''
    if request.user.is_authenticated:
        return redirect('homepage:homePage')

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
                    messages.success(request, 'Đăng kí thành công. Chào mừng đến với BKvivu.')
                    return redirect('homepage:registerPage')
            messages.error(request, 'Đăng kí không thành công. Vui lòng thử lại.')
        elif 'login' in request.POST:
            username = request.POST.get('username')
            psw = request.POST.get('password')
            user_logged = authenticate(request, username=username, password=psw)
            if user_logged is not None:
                login(request, user_logged)
                messages.success(request, 'Đăng nhập thành công rùi nhé.')
                return redirect('homepage:homePage')
            messages.error(request, 'Đăng nhập không thành công. Vui lòng thử lại.')

    # messages.error(request, 'Đăng nhập')
    return render(request, 'login.html')

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

def test(request):
    return render(request, 'manager.html')
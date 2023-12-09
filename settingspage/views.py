from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from homepage.models import *
from .forms import *
from .urls import *



# Create your views here.
def settingsPage(request):
    return redirect('settingspage:gerenalPage')

def postPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    if request.method == 'POST':
        post = Post.objects.create(account = acc)
        img = Image.objects.create(post = post)
        form_post= CreatePostForm(request.POST, request.FILES, instance=post)
        form_img = CreateImgForm(request.POST, request.FILES, instance=img)
        if form_post.is_valid() and form_img.is_valid() :
            # Thực hiện thay đổi avatar
            _post  = form_post.save(commit=False)
            _post.save()

            _img  = form_img.save(commit=False)
            _img.save()
            # newA.avatar: Avatar mới
            #Trả về trang cá nhân
            messages.success(request, 'Tạo bài viết thành công')
        else:
            messages.error(request, 'Thất bại')

    form_post = CreatePostForm()
    form_img = CreateImgForm()
    context = {
        'form_post': form_post,
        'form_img': form_img,
        'acc': acc,
    }
    return render(request, 'post.html', context)


#####-------- Sản phẩm -------######
# Quản lý Sản phẩm
def ProductManager(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    context = {
        'acc' : acc,
        'user' : user
    }
    return render(request, 'product.html', context)
#Tạo sản phẩm mới
class CreateProduct(View):
    def get(self, request):
        form_product = ProductForm()
        acc = Account.objects.get(user_ptr=request.user)
        context = {
            'acc' : acc,
            'form_product':form_product
        }
        return render(request, 'addproduct.html', context)
    def post(self, request):
        acc = Account.objects.get(user_ptr=request.user)
        if acc.role == 'sharer':
            return HttpResponse("Bạn cần là người quản lý để thực hiện")
        else:
            user = Manager.objects.get(account = acc)
            newProduct = Product.objects.create(provider = user)
            form_product = ProductForm(request.POST, request.FILES, instance= newProduct)
            if form_product.is_valid():
                if form_product.cleaned_data['img'].name == 'default.jpg':
                    messages.error(request, "Thêm sản phẩm thất bại vì thiếu hình ảnh") 
                    newProduct.delete()
                    return redirect('settingspage:product')
                product = form_product.save(commit= False) # Đối tượng mô hình k đưa vào cơ sở dữ liệu
                product.save()
                messages.success(request, "Thêm sản phẩm thành công")
            else:
                newProduct.delete()
                messages.error(request, "Thêm sản phẩm thất bại")
            return redirect('settingspage:product')


#Xóa Sản phẩm
def deleteProduct(request, product_id):
    try:
        product = Product.objects.get(pk = product_id)
        product.delete()
        messages.success(request, "Đã xóa sản phẩm")
    except:
        messages.error(request, "Thao tác lỗi")
    return redirect('settingspage:product')

# Sửa sản phẩm
class editProduct(View):
    def get(self, request, product_id):
        acc = Account.objects.get(user_ptr=request.user)
        user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
        _product = Product.objects.get(pk = product_id)
        pform = ProductForm(instance= _product)
        context = {
            'form_product': pform,
            'acc': acc, 
        }
        return render(request, 'addproduct.html', context)
    def post(sefl, request, product_id):
        _product = Product.objects.get(pk = product_id)
        pform = ProductForm(request.POST, request.FILES, instance = _product)
        if pform.is_valid():
            pform.save()
            messages.success(request, "Đã lưu thay đổi")
        else :
            messages.error(request, "Thực hiện bị lỗi")
        return redirect('settingspage:product')


def generalPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)

    if request.method == 'POST':
        if acc.role == 'sharer':
            form = UpdateSharerForm(request.POST, request.FILES, instance=user)
        else:
            form = UpdateManagerForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Thực hiện thay đổi avatar
            newA  =form.save(commit=False)
            newA.save()
            # newA.avatar: Avatar mới
            #Trả về trang cá nhân
            messages.success(request, 'Thông tin đã được cập nhật')

    form_general = UpdateSharerForm(instance= user) if acc.role == 'sharer' else UpdateManagerForm(instance=user)

    context = {
        'form_gerenal': form_general,
        'acc': acc,
    }
    return render(request, 'general.html', context)

#Bill Page
def billsPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    bills = user.bill_set.all()
    context = {
        "bills" : bills,
        "acc" : acc,
        "user" : user,
    }
    return render(request, "bills.html", context)


def viewBill(request, billId):
    if request.method == 'GET' : 
        bill = Bill.objects.get(id = billId)
        return render(request, "bill.html", {"bill" : bill})
def accept(request, billId):
    try :
        bill = Bill.objects.get(pk = billId)
        bill.status = "Accept"
        bill.save()
        # bill.delete()
        messages.success(message='Accept', request=request)
        return redirect('settingspage:billsPage')
    except : 
        messages.success(message='Error happened, try again', request=request)
        return redirect('settingspage:billsPage')
def decline(request,billId):
    try : 
        bill = Bill.objects.get(pk = billId)
        bill.status = "Decline"
        bill.save()
        # bill.delete()
        messages.success(message='Decline', request=request)
        return redirect('settingspage:billsPage')
    except :
        messages.success(message='Error happened, try again', request=request)
        return redirect('settingspage:billsPage')





#Sattistics Page
def statisticsPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    return render(request, 'statistics.html', {'acc' : acc})
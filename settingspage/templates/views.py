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



# Create your views here.
def settingsPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    return render(request, 'settings.html', {'acc' : acc})
# Post Page
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
        'acc' : acc
    }
    return render(request, 'post.html', context)




#General Page
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

    form_general = UpdateSharerForm() if acc.role == 'sharer' else UpdateManagerForm()

    context = {
        'form_gerenal': form_general,
        'acc' : acc
    }
    return render(request, 'general.html', context)





#Product Page
class ProductPage(View):
    def get(self, request,*args, **kwargs):
        acc = Account.objects.get(user_ptr=request.user)
        user = Sharer.objects.get(account=acc) if (acc.role == 'sharer') else Manager.objects.get(account=acc)
        products = user.product_set.all()
        formAdd = CreateAddProductForm()
        context = {
            "products" : products,
            "acc" : acc,
            "user" : user,
            "formAdd" : formAdd,
        }
        return render(request, "foods.html", context)
    def post(self, request,*args, **kwargs):
        acc = Account.objects.get(user_ptr=request.user)
        user = Sharer.objects.get(account=acc) if (acc.role == 'sharer') else Manager.objects.get(account=acc)
        products = user.product_set.all()
        newProduct = Product.objects.create(provider = user)
        form = CreateAddProductForm(request.POST, request.FILES, instance=newProduct)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(message='Thêm sản phẩm mới thành công', request=request)
            return redirect("settingspage:foodsPage")
        else:
            messages.error(message='Thêm sản phẩm mới thất bại', request=request)  
            return redirect("settingspage:foodsPage")
    def dispatch(self, request, *args, **kwargs):
        # Additional common logic can go here before calling get or post
        return super().dispatch(request, *args, **kwargs)
def deleteProduct(request, productId):
    product = Product.objects.get(id = productId)
    try : 
        product.delete()
        messages.success(message='Xóa sản phẩm thành công', request=request)
        return redirect('settingspage:foodsPage')
    except:
        messages.error(message='Xóa sản phẩm thất bại', request=request)
        return redirect('settingspage:foodsPage')
class ChangeProduct(View):
    def get(self, request, productId):
        product = Product.objects.get(pk = productId)
        formChange = CreateAddProductForm(instance=product)
        context = {
            'formChange' : formChange
        }
        return render(request, 'change_product.html', context)
    def post(self, request, productId):
        product = Product.objects.get(id = productId)
        form = CreateAddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid : 
            newProduct = form.save(commit=False)
            newProduct.save()
            messages.success(message='Cập nhật sản phẩm thành công', request=request)
            return redirect('settingspage:foodsPage')
        else :
            messages.success(message='Cập nhật sản phẩm thất bại', request=request)
            return redirect('settingspage:foodsPage')
        



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
        bill.delete()
        messages.success(message='Accept', request=request)
        return redirect('settingspage:billsPage')
    except : 
        messages.success(message='Error happened, try again', request=request)
        return redirect('settingspage:billsPage')
def decline(request,billId):
    try : 
        bill = Bill.objects.get(pk = billId)
        bill.status = "Decline"
        bill.delete()
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
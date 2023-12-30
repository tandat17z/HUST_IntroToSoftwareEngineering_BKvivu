from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from homepage.models import *
from .forms import *
from django.http import JsonResponse
import json
from .urls import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from collections import OrderedDict


ImageUploadFormSet = modelformset_factory(Image, CreateImgForm, extra=0, can_delete=True)


# Create your views here.
def settingsPage(request):
    return redirect('settingspage:gerenalPage')



#####-------- Sản phẩm -------######
# ProductPage
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

#generalPage
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
            newA = form.save(commit=False)
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
    # if request.method == 'POST':
    #     data_from_js = request.POST.get('data_from_js', '')
    #     acc = Account.objects.get(user_ptr=request.user)
    #     user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    #     bills = user.bill_set.all()
    
    #     context = {
    #         "bills" : bills,
    #         "acc" : acc,
    #         "user" : user,
    #         "data_from_js" : data_from_js,
    #     }
    #     messages.success(request, data_from_js)
    #     return render(request, "bills.html", context)

        # return JsonResponse({'data_from_js' : data_from_js})
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    bills = user.bill_set.all()
    selected_data = request.GET.get('selectedData', 'Waiting')
    context = {
        "bills" : bills,
        "acc" : acc,
        "user" : user,
        "data_from_js" : selected_data,
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






#Post Page
def postPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    context = {
        'acc' : acc,
        'user' : user,
    }
    return render(request, 'post.html', context)

def deletePost(request, postId):
    post = Post.objects.get(id = postId)
    try: 
        post.delete()
        messages.success(request, 'Xóa bài viết thành công')
        return redirect('settingspage:postPage')
    except:
        messages.error(request, 'Xóa bài viết thất bại')
        return redirect('settingspage:postPage')
    
def changePost(request, postId):
    if request.method == 'GET':
        acc = Account.objects.get(user_ptr=request.user)
        user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
        post = Post.objects.get(id = postId)
        img = post.image_set.all()
        form_post = CreatePostForm(instance=post)
        form_img = []
        a = 0
        for i in img :
            a = a + 1 
            form_img.append(CreateImgForm(instance=i, prefix=f'form-{a}'))
        context = {
            'acc' : acc, 
            'user' : user,
            'form_post' : form_post,
            'form_img' : form_img,
            'post': post,
            'img' : img,
        }
        return render(request, 'add_post.html', context)
    elif request.method == 'POST':
        post = Post.objects.get(id = postId)
        img = post.image_set.all()
        form_post = CreatePostForm(request.POST, request.FILES, instance=post)
        form_img = []
        a = 0
        for i in img :
            a = a+1 
            if i.isDelete == True :
                i.delete()
            else :
                form_img.append(CreateImgForm(request.POST, request.FILES, prefix=f'form-{a}', instance=i))
        if form_post.is_valid : 
            for form in form_img :
                if not form.is_valid :
                    messages.error(request, 'Error')
                    return redirect('settingspage:postPage')

            newFormPost = form_post.save(commit=False)
            newFormPost.save()
            for form in form_img : 
                newImg = form.save(commit=False)
                newImg.save()

            images = request.FILES.getlist('images')
            for image in images :
                img = Image.objects.create(post = post, img = image)
                img.save()
           
            return redirect('settingspage:postPage')
        else : 
            messages.error(request, 'Error')
            return redirect('settingspage:postPage')



def addPost(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc)
    if request.method == 'POST':
        post = Post.objects.create(account = acc)
        form_post = CreatePostForm(request.POST, request.FILES, instance=post)
        if form_post.is_valid :
            # try:
            newPost = form_post.save(commit=False)
            newPost.save()
            images = request.FILES.getlist('images')
            for image in images :
                img = Image.objects.create(post = post, img = image)
                img.save()

            messages.success(request, 'Success')
            return redirect('settingspage:postPage')
            # except: 
            #     messages.error(request, 'Error')
            #     return redirect('settingspage:postPage')
        else :
            post.delete()
            messages.error(request, 'Error')
            return redirect('settingspage:postPage')
    

    form_post = CreatePostForm()
    context = {
        'form_post': form_post,
        'acc': acc,
    }
    return render(request, 'add_post.html', context)
def deleteImagePost(request, postId, imageId):
    try:
        image = Image.objects.get(id = imageId)
        image.isDelete = True
        image.save()
        return HttpResponseRedirect(reverse('settingspage:changePost', args=[postId]))
    except:
        messages.error(request, 'Error')
        return HttpResponseRedirect(reverse('settingspage:changePost', args=[postId]))
def unDelete(request, postId, imageId):
    try:
        image = Image.objects.get(id = imageId)
        image.isDelete = False
        image.save()
        return HttpResponseRedirect(reverse('settingspage:changePost', args=[postId]))
    except:
        return HttpResponseRedirect(reverse('settingspage:changePost', args=[postId]))
    



#Sattistics Page
def statisticsPage(request):
    acc = Account.objects.get(user_ptr=request.user)
    user = Sharer.objects.get(account= acc) if acc.role == 'sharer' else Manager.objects.get(account= acc) 
    bills = user.bill_set.all()
    monthOfYear = [0]*12
    year = datetime.now().year
    month = datetime.now().month
    total = 0
    for bill in bills : 
        if bill.status == 'Accept' and bill.time.year == year :
            month = bill.time.month
            monthOfYear[month-1] += bill.price
            total += bill.price
    listRevenue = json.dumps(monthOfYear)

    product_quantity = OrderedDict()
    for product in user.product_set.all():
        product_quantity[product.name] = 0
    user_set = set()
    for bill in bills :
        if bill.status == 'Accept' and bill.time.year == year and bill.time.month == month:
            for order in  bill.order_set.all():
                product = Product.objects.get(id=order.product_id)
                product_quantity[product.name] += order.quantity
            user_set.add(Sharer.objects.get(account_id=bill.sharer_id))
    age_list = [0]*4
    total_age = len(user_set)
    for u in user_set:
        age = u.age
        if age >= 10 and age < 18:
            age_list[0] += 1        
        elif age >= 18 and age < 30:
            age_list[1] += 1
        elif age >= 30 and age < 50:
            age_list[2] += 1
        else:
            age_list[3] += 1
    age_phantram = [round(age_list[0]*100/total_age, 2), round(age_list[1]*100/total_age,2), round(age_list[2]*100/total_age, 2), round(age_list[3]*100/total_age, 2)]
            
    sorted_product_quantity = OrderedDict(sorted(product_quantity.items(), key = lambda item: item[1], reverse=True))
    context = {
        'acc' : acc,
        'monthOfYear' : listRevenue,
        'year' : year,
        'month': month,
        'total' : total,
        'product_quantity' : sorted_product_quantity,
        'product': user.product_set.all(),
        'best_seller_name' : next(iter(sorted_product_quantity.items()))[0],
        'best_seller_quantity' : next(iter(sorted_product_quantity.items()))[1],
        'age_phantram': json.dumps(age_phantram),
    }
    return render(request, 'statistics.html', context)
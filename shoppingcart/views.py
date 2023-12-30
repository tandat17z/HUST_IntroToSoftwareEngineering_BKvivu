from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import logout
from collections import defaultdict
from .models import *
from .forms import *
from homepage.models import *


#Shopping Cart
def viewShoppingCart(request):
    if request.user.is_authenticated:
        #Tài khoản đang đăng nhập hệ thống
        acc = Account.objects.get(user_ptr=request.user)
        user_cart_items = CartItem.objects.filter(account= acc)
        #Tạo danh sách products theo cửa hàng
        items_in_cart = dict()
        for item in user_cart_items:
            manager = item.product.provider  # Thay 'manager' bằng trường hoặc liên kết mà bạn sử dụng để chỉ đến Manager
            if manager in items_in_cart.keys():
                items_in_cart[manager].append(item)
            else:
                items_in_cart[manager] = [item,]

        context = {
            'items_in_cart' : items_in_cart,
        }
        return render(request, 'shoppingcart/shoppingCart.html', context)
    else :
        messages.error("Bạn cần đăng nhập để thực hiện thao tác này")
        return redirect('homepage:loginPage')

# Thêm sản phẩm vào giỏ hàng
def addItemToCart(request, product_id):
    # acc, user : Bản thân người đang đăng nhập
    acc = Account.objects.get(user_ptr=request.user)
    product = Product.objects.get(pk = product_id)
    target_acc_id = product.provider.account.id
    # Lấy (Tạo) cartItem
    cart_item, created = CartItem.objects.get_or_create(account=acc, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('profilepage:profilePage', acc_id=target_acc_id)

# Cập nhật, xóa dữ liệu sản phẩm trong giỏ hàng
@csrf_exempt
def updateQuantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')
        # Lấy đối tượng ItemCart từ cơ sở dữ liệu
        item = CartItem.objects.get(pk=item_id)

        if action == 'increase':
            item.quantity += 1
            item.save()
        elif action == 'decrease':
            item.quantity -= 1 if item.quantity > 0 else 0
            item.save()
        elif action == 'removeitem':
            item.delete()

        return JsonResponse({'message': 'Số lượng đã được cập nhật'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

# Tạo hóa đơn thanh toán
def createBill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #Dữ liệu các id của các lựa chọn trong giỏ hàng
        item_ids = data.get('selectedItems')
        manager_id = int(data.get('manager_id'))
        manager = CartItem.objects.get(pk = item_ids[0]).product.provider
        # Tạo đối tượng Bill
        new_bill = Bill.objects.create(
            acc = Account.objects.get(user_ptr=request.user),
            provider = manager,
            time = timezone.now()
        )
        # Tạo order cho mỗi items
        for item_id in item_ids:
            item = CartItem.objects.get(pk = item_id)
            _product = item.product
            _quantity = item.quantity
            if _product.provider.account.id == manager_id:
                item.delete()
                new_bill.price += _product.price * _quantity
                print(new_bill.price)
                new_order = Order.objects.create(
                    bill = new_bill,
                    product = _product,
                    quantity = _quantity
                )
        #Lưu lại giá
        new_bill.save()
        return JsonResponse({'bill_id': new_bill.id ,'messages': 'Tạo bill thành công'})

    else :
        print("thất bại")
        return JsonResponse({'error': 'Tạo bill thất bại'})

#Hiển thị trang thanh toán
class Payment(View):
    def get(self, request, bill_id):
        acc = Account.objects.get(user_ptr = request.user)
        bill = Bill.objects.get(pk = bill_id)
        manager = bill.provider
        form_pay = BillForm(instance= bill)
        context = {
            'acc' : acc,
            'bill' : bill,
            'form_pay' : form_pay,
            'manager' : manager
        }
        return render(request, 'shoppingcart/paymentPage.html', context)
    def post(self, request, bill_id):
        acc = Account.objects.get(user_ptr = request.user)
        bill = Bill.objects.get(pk = bill_id)
        manager = bill.provider
        form_pay = BillForm(request.POST, request.FILES, instance= bill)
        if form_pay.is_valid():
            form_pay.save()
        context = {
            'acc' : acc,
            'bill' : bill,
            'form_pay' : form_pay,
            'manager' : manager
        }
        return HttpResponse("Hóa đơn thanh toán của bạn đang được xác nhận")

# Xóa bill và các order liên quan ở database
def cancelPayment(request, bill_id):
    bill = Bill.objects.get(pk = bill_id)
    bill.delete()
    return redirect('shoppingcart:shoppingCart')
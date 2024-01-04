from django.urls import path, include
from . import views

app_name = 'shoppingcart'
urlpatterns = [
    path('', views.viewShoppingCart, name ='shoppingCart'),
    path('additem/<int:product_id>/', views.addItemToCart, name='addItem'),
    path('update_quantity/', views.updateQuantity, name='updateQuantity'),
    path('create_bill/', views.createBill, name='createBill'),
    path('payment/<int:bill_id>/', views.Payment.as_view(), name='paymentPage'),
    path('cancelpayment/<int:bill_id>/', views.cancelPayment, name = 'cancelPayment'),
    path('orderlist/', views.OrderList.as_view(), name= 'orderList'),

]
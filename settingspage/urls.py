from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'settingspage'
urlpatterns = [
    path('', views.settingsPage, name='settingsPage'),
    path('general/', views.generalPage, name='gerenalPage'),
    path('posts/', views.postPage, name='postPage'),
    path('product/', views.ProductManager, name='product'),
    path('products/add', views.CreateProduct.as_view(), name='addProduct'),
    path('product/delete/<int:product_id>', views.deleteProduct, name='deleteProduct'),
    path('product/edit/<int:product_id>', views.editProduct.as_view(), name='editProduct'),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)
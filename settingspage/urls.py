from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'settingspage'
urlpatterns = [
    path('', views.settingsPage, name='settingsPage'),
    path('general/', views.generalPage, name='gerenalPage'),

    path('posts', views.testPostPage, name='testPostPage'),
    path('posts/addPosts', views.testCreatePosts, name='testCreatePosts'),
    path('posts/delete/<int:postId>/', views.testDeletePost, name='testDeletePosts'),
    # path('posts/', views.postPage, name='postPage'),
    path('posts/changePost/<int:postId>', views.changePost, name='changePost'),
    path('posts/addPost', views.addPost, name='addPost'),
    path('posts/deletePost/<int:postId>', views.deletePost, name='deletePost'),
    path('posts/changePost/<int:postId>/deleteImagePost/<int:imageId>', views.deleteImagePost, name='deleteImagePost'),
    path('posts/changePost/<int:postId>/unDelete/<int:imageId>', views.unDelete, name='unDelete'),
    
    path('product/', views.ProductManager, name='product'),
    path('product/add', views.CreateProduct.as_view(), name='addProduct'),
    path('product/delete/<int:product_id>', views.deleteProduct, name='deleteProduct'),
    path('product/edit/<int:product_id>', views.editProduct.as_view(), name='editProduct'),


    path('bills/', views.billsPage, name='billsPage'),
    path('bills/viewBill/<int:billId>', views.viewBill, name='viewBill'),
    path('bills/viewBill/<int:billId>/accept/>', views.accept, name='accept'),
    path('bills/viewBill/<int:billId>/decline/>', views.decline, name='decline'),


    path('statistics/', views.statisticsPage, name='statisticsPage'),

    # path('test', views.test, name='test'),
    # path('test/addPosts', views.testCreatePosts, name='testCreatePosts'),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)
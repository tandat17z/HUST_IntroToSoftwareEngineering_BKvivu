from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'settingspage'
urlpatterns = [
    path('', views.settingsPage, name='settingsPage'),
    path('general/', views.generalPage, name='gerenalPage'),
    path('posts/', views.postPage, name='postPage'),
    path('foods/',views.ProductPage.as_view(), name='foodsPage'),
    path('foods/changeProduct/<int:productId>', views.ChangeProduct.as_view(), name='changeProduct'),
    path('foods/deleteProduct/<int:productId>', views.deleteProduct, name='deleteProduct'),
    path('bills/', views.billsPage, name='billsPage'),
    path('bills/viewBill/<int:billId>', views.viewBill, name='viewBill'),
    path('bills/viewBill/<int:billId>/accept/>', views.accept, name='accept'),
    path('bills/viewBill/<int:billId>/decline/>', views.decline, name='decline'),
    path('statistics/', views.statisticsPage, name='statisticsPage'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_URL)
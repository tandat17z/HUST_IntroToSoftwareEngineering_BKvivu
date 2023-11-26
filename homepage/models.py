import os
from django.db import models
from django.contrib.auth.models import User
import django.db.models.deletion

def image_upload_path(instance, filename):
    """Hàm callback để đặt tên cho tệp hình ảnh được tải lên."""
    username = instance.username 
    role = instance.role 
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"{username}.{ext}"  # Đặt tên mới

    return os.path.join('avatar', role , new_filename)
    
    
# Create your models here.---------------------------------------------------
class Account(User):
    ROLES = [
        ('sharer', 'Người chia sẻ'),
        ('manager', 'Người quản lý'),
    ]
    raw_password = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=10, choices=ROLES)
    avatar = models.ImageField(upload_to=image_upload_path, default='default.jpg')
    # class Meta:
    #     db_table = 'auth_user'

    def __str__(self):
        return f"{self.username}"
    

class Sharer(models.Model):
    account = models.OneToOneField(Account, on_delete=django.db.models.deletion.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.account.username}"
    

class Manager(models.Model):
    account = models.OneToOneField(Account, on_delete=django.db.models.deletion.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.account.username}"
    
class Product(models.Model):
    pass

class Post(models.Model):
    # account = 
    pass
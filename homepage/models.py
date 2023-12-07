import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import django.db.models.deletion
from django.utils import timezone


# Xử lý lưu trữ hình ảnh --------------------------------------------------
def img_path_avt(instance, filename):
    acc = instance.account
    username = acc.username
    role = acc.role
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"avatar.{ext}"  # Đặt tên mới
    return os.path.join(role, username , new_filename)

def imgs_path(instance, filename):
    post_name = str(instance.post)
    username = str(instance.post.account)
    role = instance.post.account.role
    return os.path.join(role, username , 'posts', post_name, filename)


def img_path_bill(instance, filename):
    provider_name = str(instance.provider)
    sharer_name = str(instance.sharer)
    time = instance.time
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"{time}_{sharer_name}.{ext}"  # Đặt tên mới
    return os.path.join('manager', provider_name, 'bills', new_filename)

def img_path_product(instance, filename):
    username = instance.provider.account.username
    product_name = instance.name
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"{product_name}.{ext}"  # Đặt tên mới
    return os.path.join('manager', username, 'products', new_filename)


# Create your models here.---------------------------------------------------
class Account(User):
    ROLES = [
        ('sharer', 'Người chia sẻ'),
        ('manager', 'Người quản lý'),
    ]
    raw_password = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=10, choices=ROLES)
    # avatar = models.ImageField(upload_to=img_path_avt, default='noavatar.png')

    def __str__(self):
        return f"{self.username}"


class Sharer(models.Model):
    account = models.OneToOneField(Account, on_delete=django.db.models.deletion.CASCADE, primary_key=True)
    name = models.CharField(verbose_name='fullname', max_length=50)
    avatar = models.ImageField(upload_to=img_path_avt, default='noavatar.png')

    def __str__(self):
        return f"{self.account}"
    def save(self, *args, **kwargs):
        # Kiểm tra và xóa ảnh cũ (nếu có)
        if self.pk:
            try:
                old_instance = Sharer.objects.get(pk=self.pk)
                check = True
            except:
                check = False

            if check and old_instance.avatar.name != 'noavatar.png':
                if old_instance.avatar:
                    old_instance.avatar.delete(save=False)
        # Gọi hàm save của lớp cha (object)
        super().save(*args, **kwargs)

class Manager(models.Model):
    account = models.OneToOneField(Account, on_delete=django.db.models.deletion.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to=img_path_avt, default='noavatar.png')

    address = models.TextField(null=True)
    bio = models.TextField(max_length=1500, null = True)

    num_stars = models.IntegerField(null=True, default=0)
    num_votes = models.IntegerField(null=True, default=0)
    rank = models.FloatField(null=True, default=0)

    def __str__(self):
        return f"{self.account}"

    def save(self, *args, **kwargs):
        # Kiểm tra và xóa ảnh cũ (nếu có)
        if self.pk:
            try:
                old_instance = Manager.objects.get(pk=self.pk)
                check = True
            except:
                check = False
            if check and old_instance.avatar.name != 'noavatar.png':
                if old_instance.avatar:
                        old_instance.avatar.delete(save=False)

        # tự động tính rank = star/ vote
        if self.num_votes > 0:
            self.rank = round(self.num_stars / self.num_votes, 2)
        else:
            self.rank = 0
        # Gọi hàm save của lớp cha (object)
        super().save(*args, **kwargs)

class Product(models.Model):
    TYPES = [
        ('food', 'Đồ ăn'),
        ('service', 'Dịch vụ khác'),

    ]
    provider = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.TextField()
    type = models.CharField(max_length=10, choices=TYPES)
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to=img_path_product, default='default.jpg')
    describe = models.TextField(null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.datetime.now())

    def __str__(self):
        return f"{self.provider}_{self.name}"

class Bill(models.Model):
    sharer = models.ForeignKey(Sharer, on_delete=models.SET_NULL, null=True, verbose_name='Người mua')
    provider = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(default=timezone.datetime.now())
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to=img_path_bill, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.provider}_{self.sharer}_" + datetime.strftime(self.time, "%Y-%m-%d %H:%M:%S")

class Order(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product}_{self.bill}"

class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    time = models.DateTimeField(default=timezone.datetime.now())
    location = models.TextField()
    provider = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.account}_{self.title}"

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to=imgs_path)

    def __str__(self):
        return f"{self.post}"

class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=django.db.models.deletion.CASCADE)
    content = models.TextField()
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post}"


# vote_profile_model
class StarVote(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)

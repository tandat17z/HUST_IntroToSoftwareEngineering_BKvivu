import os
from unidecode import unidecode
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import django.db.models.deletion
from django.db.models import Avg
from django.utils import timezone
import uuid

# Xử lý lưu trữ hình ảnh --------------------------------------------------
def img_path_avt(instance, filename):
    acc = instance.account
    username = acc.username
    role = acc.role
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"avatar.{ext}"  # Đặt tên mới
    return os.path.join(role, username , new_filename)

def img_path_bank(instance, filename):
    acc = instance.account
    username = acc.username
    role = acc.role
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"bank.{ext}"  # Đặt tên mới
    return os.path.join(role, username , new_filename)

def imgs_path(instance, filename):
    post_name = str(instance.post)
    username = str(instance.post.account)
    role = instance.post.account.role
    return os.path.join(role, username , 'posts', post_name, filename)

def img_path_bill(instance, filename):
    provider_name = str(instance.provider)
    acc_name = str(instance.acc)
    time = instance.time
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"{time}_{acc_name}.{ext}"  # Đặt tên mới
    return os.path.join('manager', provider_name, 'bills', new_filename)

def img_path_product(instance, filename):
    username = instance.provider.account.username
    product_name = instance.name
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"{product_name}.{ext}"  # Đặt tên mới
    return os.path.join('manager', username, 'products', new_filename)

def generate_unique_post_id():
    return str(uuid.uuid4())

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
    age = models.IntegerField(null = True)
    avatar = models.ImageField(upload_to=img_path_avt, default='noavatar.png')

    city = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    ward = models.CharField(max_length=50, null=True)

    bio = models.TextField(max_length=1500, null = True)

    def __str__(self):
        return f"{self.account}"
    
    # def save(self, *args, **kwargs):
    #     # Kiểm tra và xóa ảnh cũ (nếu có)
    #     if self.pk:
    #         try:
    #             old_instance = Sharer.objects.get(pk=self.pk)
    #             check = True
    #         except:
    #             check = False

    #         if check and old_instance.avatar.name != 'noavatar.png':
    #             if old_instance.avatar:
    #                 old_instance.avatar.delete(save=False)
    #     # Gọi hàm save của lớp cha (object)
    #     super().save(*args, **kwargs)

class Manager(models.Model):
    account = models.OneToOneField(Account, on_delete=django.db.models.deletion.CASCADE, primary_key=True)

    name = models.TextField(max_length=50)
    name_stripped = models.TextField(max_length=50, null=True)# Thêm thuộc tính name_stripped tự động lưu sẽ bỏ dấu câu trong name-----

    phone = models.CharField(max_length=15, null=True)
    avatar = models.ImageField(upload_to=img_path_avt, default='noavatar.png')
    bank = models.ImageField(upload_to=img_path_bank, default='noavatar.png')
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    website_link = models.URLField(max_length=200, blank=True, null=True)
    t_open = models.TimeField(default='0:00')
    t_closed = models.TimeField(default='23:59')

    address = models.TextField(null=True)
    city = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    ward = models.CharField(max_length=50, null=True)

    bio = models.TextField(max_length=1500, null = True)

    #x num_stars = models.IntegerField(null=True, default=0)
    #x rank = models.FloatField(null=True, default=0)

    num_votes = models.IntegerField(null=True, default=0) #tổng số lượt đánh giá
    avgStar = models.FloatField(default=0.0) #Số sao đánh giá trung bình của cửa hàng


    def __str__(self):
        return f"{self.account}"

    # Hàm cập nhật đánh giá trung bình sau mỗi lượt đánh giá
    def updateAvgStar(self):
        self.num_votes = self.starvote_set.count()
        avg_star = StarVote.objects.filter(manager=self).aggregate(Avg('stars'))['stars__avg']
        self.avgStar = avg_star if avg_star else 0.0

    # def save(self, *args, **kwargs):
    #     # Kiểm tra và xóa ảnh cũ (nếu có)
    #     if self.pk:
    #         try:
    #             old_instance = Manager.objects.get(pk=self.pk)
    #             check = True
    #         except:
    #             check = False
    #         if check and old_instance.avatar.name != 'noavatar.png':
    #             if old_instance.avatar:
    #                     old_instance.avatar.delete(save=False)
    #         if check and old_instance.bank.name != 'noavatar.png':
    #             if old_instance.bank:
    #                     old_instance.bank.delete(save=False)

        #x tự động tính rank = star/ vote
        #x if self.num_votes > 0:
        #x     self.rank = round(self.num_stars / self.num_votes, 2)
        #x else:
        #x     self.rank = 0

        # Gọi hàm tính sao trung bình để cập nhật avgStar
        # self.updateAvgStar()

        # bỏ dấu của name để phục vụ tính năng tìm kiếm
        # if self.name:
        #     words = unidecode(self.name.lower()).split()
        #     self.name_stripped = ' '.join(words)

        # Gọi hàm save của lớp cha (object)
        # super().save(*args, **kwargs)

class Product(models.Model):
    TYPES = [
        ('food', 'Đồ ăn'),
        ('bun dau', 'Bún đậu'),
        ('com rang', 'Cơm rang'),
        ('nem nuong', 'Nem nướng'),
        ('cong vien', 'Công viên'),
        ('bao tang', 'Bảo tàng'),
        ('service', 'Dịch vụ khác'),
    ]
    provider = models.ForeignKey(Manager, on_delete=models.CASCADE)

    name = models.TextField()
    # Thêm thuộc tính name_stripped tự động lưu sẽ bỏ dấu câu trong name-----
    name_stripped = models.TextField(max_length=50, null=True)

    type = models.CharField(max_length=10, choices=TYPES)
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to=img_path_product, default='default.jpg')
    describe = models.TextField(null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.datetime.now())

    def __str__(self):
        return f"{self.provider}_{self.name}"

    def save(self, *args, **kwargs):
        if self.name:
            words = unidecode(self.name.lower()).split()
            self.name_stripped = ' '.join(words)
        super().save(*args, **kwargs)

class Bill(models.Model):
    STATUS = [
        
    ]
    acc = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='Người mua')
    provider = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(default=timezone.datetime.now())
    price = models.IntegerField(default=0)
    img = models.ImageField(upload_to=img_path_bill, null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS, default='Waiting')

    def __str__(self):
        return f"{self.provider}_{self.acc}_" + datetime.strftime(self.time, "%Y-%m-%d %H:%M:%S")

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
    name_stripped = models.CharField(max_length=150000, null=True)
    time = models.DateTimeField(default=timezone.datetime.now())

    address = models.TextField(null=True)
    city = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True)
    ward = models.CharField(max_length=50, null=True)

    provider = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    commentNum = models.IntegerField(default= 0)

    def __str__(self):
        return f"{self.account}_{self.title}"

    def save(self, *args, **kwargs):
        words = unidecode((self.title + " " + self.content).lower()).split()
        self.name_stripped = ' '.join(words)

        #Tự động tính số like
        likeList = UserLike.objects.filter(post = self)
        self.like = likeList.count()
        super().save(*args, **kwargs)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    img = models.ImageField(upload_to=imgs_path)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.post}"


# vote_profile_model
class StarVote(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.account} Voted For {self.manager}"

# item in shoppingCart
class CartItem(models.Model):
    account = models.ForeignKey(Account, on_delete = models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.product} in shopping Cart of {self.account}"

# like + comment
class UserLike(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null= True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    # class Meta:
    #     # primary key ( account,post)
    #     constraints = [
    #         models.UniqueConstraint(fields=['account_id', 'post_id'], name='unique_constraint_name')
    #     ]

class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=django.db.models.deletion.CASCADE)
    time = models.DateTimeField(default=timezone.datetime.now())
    content = models.TextField()
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post}"

class Test(models.Model):
    content = models.TextField()
#Model for chatPage
class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, related_name='send')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, null= False, related_name='recieve')
    content = models.CharField(max_length=1000)
    time = models.DateTimeField(default=timezone.datetime.now())
    def __str__(self):
        return f"{self.sender} to {self.receiver} ({self.time})"
class ImageMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    img = models.ImageField()

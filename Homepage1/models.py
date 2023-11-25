import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def image_upload_path(instance, filename):
    """Hàm callback để đặt tên cho tệp hình ảnh được tải lên."""
    username = instance.username 
    ext = filename.split('.')[-1]  # Lấy phần mở rộng của tệp
    new_filename = f"{username}.{ext}"  # Đặt tên mới

    return os.path.join('avatar_user/', new_filename)


class TaiKhoan(models.Model):
    VAITRO = [
        ('m', 'NguoiQuanLy'),
        ('u', 'NguoiChiaSe'),
    ]
    
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    vaitro = models.CharField(max_length=1, choices=VAITRO)
    avatar = models.ImageField(upload_to=image_upload_path, default=os.path.join('avatar_user/', 'default.png'))

    def __str__(self) -> str:
        return f"{self.username}"
    
    def save(self, *args, **kwargs):
        # Kiểm tra sự thay đổi và xóa hình ảnh cũ
        if self.pk:
            old_instance = TaiKhoan.objects.get(pk=self.pk)
            if old_instance.avatar != self.avatar:
                if old_instance.avatar:
                    old_instance.avatar.delete(save=False)
        super(TaiKhoan, self).save(*args, **kwargs)
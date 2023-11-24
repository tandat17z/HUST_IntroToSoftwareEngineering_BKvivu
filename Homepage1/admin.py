from django.contrib import admin
from .models import *

# Register your models here.
class TaiKhoanAdmin(admin.ModelAdmin):
    list_display = ("username", "password", "vaitro", "avatar")

admin.site.register(TaiKhoan, TaiKhoanAdmin)
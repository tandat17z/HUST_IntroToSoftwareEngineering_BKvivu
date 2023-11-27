from django.contrib import admin
from .models import *

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'raw_password', 'role', 'avatar')

class SharerAdmin(admin.ModelAdmin):
    list_display = ('account', 'name')

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('account', 'name', 'address')

class BillAmin(admin.ModelAdmin):
    list_display = ('__str__', 'time', 'status')
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'time', 'location', 'provider', 'like', 'dislike')
admin.site.register(Account, AccountAdmin)
admin.site.register(Sharer, SharerAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Product)
admin.site.register(Bill, BillAmin)
admin.site.register(Order)
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment)
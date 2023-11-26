from django.contrib import admin
from .models import *

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'raw_password', 'role', 'avatar')

class SharerAdmin(admin.ModelAdmin):
    list_display = ('account', 'name')

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('account', 'name', 'address')

admin.site.register(Account, AccountAdmin)
admin.site.register(Sharer, SharerAdmin)
admin.site.register(Manager, ManagerAdmin)
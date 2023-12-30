from django.contrib import admin
from .models import *

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'raw_password', 'role')

class SharerAdmin(admin.ModelAdmin):
    list_display = ('account', 'name')

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('account', 'name', 'address', 'avgStar')

class BillAmin(admin.ModelAdmin):
    list_display = ('__str__', 'time', 'status')

class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'time', 'provider', 'like', 'dislike')
    
class UserLikeAdmin(admin.ModelAdmin):
    list_display = ('account', 'post')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content')
admin.site.register(Account, AccountAdmin)
admin.site.register(Sharer, SharerAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Product)
admin.site.register(Bill, BillAmin)
admin.site.register(Order)
admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment, CommentAdmin)
admin.site.register(StarVote)
admin.site.register(UserLike, UserLikeAdmin)
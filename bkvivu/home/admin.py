from django.contrib import admin
from .models import Home

# Register your models here.

class HomeAdmin(admin.ModelAdmin):
  list_display = ("firstname", "lastname", "joined_date",)
admin.site.register(Home, HomeAdmin)
from django import forms
from homepage.models import *

# class UploadAvatar(forms.ModelForm):
#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = 'ModelName'
#         verbose_name_plural = 'ModelNames'
#     avatar = forms.ImageField( required=False)

class UploadAvatar(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("avatar",)



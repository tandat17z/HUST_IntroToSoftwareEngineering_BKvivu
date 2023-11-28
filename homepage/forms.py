from django import forms
from .models import *

class CreateAccountForm(forms.Form):
    ROLES = [
        ('sharer', 'Người chia sẻ'),
        ('manager', 'Người quản lý'),
    ]
    role = forms.ChoiceField(choices=ROLES)
    # name = forms.CharField(max_length=50, required=False)

class AccountAvatarForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('avatar',)

class CreateSharerForm(forms.ModelForm):
    account = AccountAvatarForm()
    class Meta:
        model = Sharer
        fields = ('name', 'account')

class CreateManagerForm(forms.ModelForm):
    account = AccountAvatarForm()
    class Meta:
        model = Manager
        fields = ('name', 'address', 'account')
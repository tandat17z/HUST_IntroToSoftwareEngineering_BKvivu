from django import forms
from .models import *

class CreateAccountForm(forms.Form):
    ROLES = [
        ('sharer', 'Người chia sẻ'),
        ('manager', 'Người quản lý'),
    ]
    role = forms.ChoiceField(choices=ROLES)
    name = forms.CharField(max_length=50, required=False)

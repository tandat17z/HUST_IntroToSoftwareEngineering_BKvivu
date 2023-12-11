from django import forms
from .models import *

class CreateAccountForm(forms.Form):
    ROLES = [
        ('sharer', 'Người chia sẻ'),
        ('manager', 'Người quản lý'),
    ]
    role = forms.ChoiceField(choices=ROLES)
    # name = forms.CharField(max_length=50, required=False)

class FormSearchChooseArea(forms.Form):
    AREA = Manager.AREA
    area = forms.ChoiceField(choices=AREA)
    
class CreateSharerForm(forms.ModelForm):
    class Meta:
        model = Sharer
        fields = ('name',)

class CreateManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ('name', 'address',)
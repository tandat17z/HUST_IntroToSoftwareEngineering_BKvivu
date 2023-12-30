from django import forms
from homepage.models import *

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ('img', )
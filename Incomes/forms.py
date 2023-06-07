from django import forms
from .models import *

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = '__all__'
    
class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ('price','last_update', 'update_frequency')
        
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('date','resident','income')
        
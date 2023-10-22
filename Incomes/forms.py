from django import forms
from .models import *

class ResidentForm(forms.ModelForm):
    class Meta:
        model = Residente
        # fields = '__all__'
        fields = ('nombre', 'apellido' , 'apodo' , 'dni')
    
class FeeForm(forms.ModelForm):
    class Meta:
        model = Cuota
        fields = ('precio','ultima_actualizacion', 'frecuencia_actualizaciones')
        
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ('fecha','residente','monto','mes','anio')

        
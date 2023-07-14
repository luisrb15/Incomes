from django.shortcuts import redirect, render
from .forms import *
from .models import Residente

# Create your views here.

def home(request):  
    return render(request, 'home.html')

def incomes_form(request):
    form = IncomeForm()
    context = {'form' : form}
    return render(request, 'ingresos-form.html', context)

def residentes(request):
    residentes_lista = Residente.objects.all
    context = {'residentes': residentes_lista}
    return render(request, 'residentes.html', context)

def residentes_form(request, id):
    form = ResidentForm()
    residente = Residente.objects.get(pk = id)
    context = {'form' : form, 'residente' : residente}
    return render(request, 'residente-form.html', context)
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from .models import Residente
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):  
    return render(request, 'home.html')

def incomes_form(request):
    form = IncomeForm()
    context = {'form' : form}
    return render(request, 'ingresos-form.html', context)

def residentes(request):
    residentes_lista = Residente.objects.filter()
    context = {'residentes': residentes_lista}
    return render(request, 'residentes.html', context)

def residente_agregar(request):
    form = ResidentForm()
    context = {'form' : form }
    return render(request, 'residente-form.html', context)

def residentes_form(request, pk):
    residente = get_object_or_404(Residente, pk=pk)
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            residente.nombre = form.cleaned_data['nombre']
            residente.apellido = form.cleaned_data['apellido']
            residente.apodo = form.cleaned_data['apodo']
            residente.dni = form.cleaned_data['dni']
            residente.active = form.cleaned_data['active']
            return HttpResponseRedirect('/')
    form = ResidentForm()
    residente = Residente.objects.get(pk = id)
    context = {'form' : form, 'residente' : residente}
    return render(request, 'residente-form.html', context)
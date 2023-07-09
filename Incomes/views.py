from django.shortcuts import redirect, render
from .forms import IncomeForm

# Create your views here.

def home(request):  
    return render(request, 'home.html')

def incomes_form(request):
    form = IncomeForm()

    context = {'form' : form}

    return render(request, 'ingresos-form.html', context)

from django.urls import path
from . import views

app_name = 'Incomes'

urlpatterns = [
    path('', views.home),
    path('ingresos-form/', views.incomes_form, name='ingresos-form'),
]
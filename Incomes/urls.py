from django.urls import path
from . import views

app_name = 'Incomes'

urlpatterns = [
    path('', views.home),
    path('ingresos-form/', views.incomes_form, name='ingresos-form'),
    path('residentes/',views.residentes, name='residentes'),
    path('residentes/actualizar/<id>', views.residentes_form, name='residentes-actualizar'),
    path('residentes/residente-form', views.residente_agregar, name='residentes-form'),
]
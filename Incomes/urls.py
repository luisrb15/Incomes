from django.urls import path
from . import views

app_name = 'Incomes'

urlpatterns = [
    path('', views.home, name='home'),
    path('ingresos-form/', views.ingresos_form, name='ingresos_form'),
    path('residentes/',views.residentes, name='residentes'),
    path('residentes/actualizar/<id>', views.residentes_modificar, name='residentes-actualizar'),
    path('residentes/agregar', views.residente_agregar, name='residentes-crear'),
    path('residentes/eliminar/<id>', views.residentes_eliminar, name='residentes-eliminar'),
    path('residentes/cuota/<id>', views.cuota_crear, name='cuota-crear'),
    path('ingresos/restantes', views.ingresos_restantes, name='ingresos-restantes'),
    path('ingresos', views.ingresos, name='ingresos'),
]
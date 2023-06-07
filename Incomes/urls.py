from django.urls import path
from . import views

app_name = 'Incomes'

urlpatterns = [
    path('', views.home),
]
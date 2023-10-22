from django.db import models
from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator

current_year = datetime.now().year
current_month = datetime.now().month

class Residente(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    apellido = models.CharField(max_length=50, verbose_name='Apellido')
    apodo = models.CharField(max_length=50, default="sin apodo", verbose_name='Apodo')
    dni = models.IntegerField(default=00000000, verbose_name='Dni')
    email = models.EmailField(default='laflordelbambuapp@gmail.com', verbose_name='Email')
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.apodo})"
    
class Cuota(models.Model):
    residente = models.OneToOneField(Residente, on_delete=models.CASCADE, verbose_name='Residente')
    precio = models.IntegerField(default=0, verbose_name='Precio')
    ultima_actualizacion = models.DateField(verbose_name='Ultima Actualizacion')  
    frecuencia_actualizaciones = models.IntegerField(verbose_name='Frecuencia Actualizaciones') 

    def actualizacion_formateada(self):
        return self.ultima_actualizacion.strftime('%d-%m-%y')
    
    def __str__(self):
        return f"{self.residente.apellido}, {self.residente.nombre} ({self.residente.apodo}) ${self.precio}"
    
class Ingreso(models.Model):
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha')
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, verbose_name='Residente')
    monto = models.IntegerField(default="", verbose_name='Ingreso de dinero')
    mes = models.IntegerField(
        default=current_month,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12)
        ],
        verbose_name='Mes de imputacion')
    anio = models.IntegerField(
        default=current_year,
        validators=[
            MinValueValidator(2020),
            MaxValueValidator(2030)
        ], 
        verbose_name='Año de imputacion')

    def __str__(self):
        monto = "${:,.2f}".format(self.monto)
        return f"{self.residente} {monto}"

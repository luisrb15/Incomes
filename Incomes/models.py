from django.db import models
from datetime import datetime

# Create your models here.
class Residente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    apodo = models.CharField(max_length=50, default="sin apodo")
    dni = models.IntegerField(unique=True) 
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.apodo})"
    
class Cuota(models.Model):
    residente = models.OneToOneField(Residente, on_delete=models.CASCADE)
    precio = models.IntegerField(default=0)
    ultima_actualizacion = models.DateField()  
    frecuencia_actualizaciones = models.IntegerField() 
    
    def __str__(self):
        return f"{self.residente.apellido}, {self.residente.nombre} ({self.residente.apodo}) ${self.precio}"
    
class Ingreso(models.Model):
    fecha = models.DateField(default=datetime.now)
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    ingreso = models.IntegerField(default=0)
    cuota = models.ForeignKey(Cuota, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.residente} {self.ingreso}"

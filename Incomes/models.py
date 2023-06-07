from django.db import models
from datetime import datetime

# Create your models here.
class Resident(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50, default="sin apodo")
    dni = models.IntegerField(unique=True, max_length=8) 
    
    def __str__(self):
        return f"{self.last_name}, {self.name} ({self.alias})"
    
class Fee(models.Model):
    resident = models.OneToOneField(Resident, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    last_update = models.DateField()  
    update_frequency = models.IntegerField() 
    
    def __str__(self):
        return f"{self.last_name}, {self.name} ({self.alias}) ${self.price}"
    
class Income(models.Model):
    date = models.DateField(default=datetime.now)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    income = models.IntegerField(default=0)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.resident} {self.income}"

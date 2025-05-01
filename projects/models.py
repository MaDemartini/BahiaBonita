from django.db import models

# Create your models here.

class reserva(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    
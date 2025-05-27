# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class view_resumen_reserva(models.Model):
    id_reserva = models.IntegerField()
    nombre_cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=10)
    departamento_numero = models.IntegerField()
    fecha_inicio = models.DateField()  
    fecha_fin = models.DateField()  
    cantidad_de_personas = models.IntegerField()  
    tipo_de_reserva = models.CharField(max_length=20)  
    total = models.FloatField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'view_resumen_reserva'

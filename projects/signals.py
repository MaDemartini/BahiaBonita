from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Persona, Cliente
from django.db import transaction

# al crear una persona, se crea un cliente automaticamente
# esto es para que no se repita el rut y el email en la base de datos, ya que son unicos

@receiver(post_save, sender=Persona)
def create_cliente(sender, instance, created, **kwargs):
    if created:
        
        transaction.on_commit( lambda:Cliente.objects.create(
                                
                                
                                id_persona = instance,                                
                                nombre = instance.nombre,                                
                                s_nombre = instance.s_nombre,
                                apellido = instance.apellido,
                                s_apellido = instance.s_apellido, 
                                rut = instance.rut,
                                dv = instance.dv,                             
                                fecha_nacimiento = instance.fecha_nacimiento,
                                direccion = instance.direccion,
                                telefono = instance.telefono,
                                email = instance.email,                                                                
                                fecha_creacion = instance.fecha_creacion,
                                fecha_eliminacion = instance.fecha_eliminacion,
                                fecha_modificacion = instance.fecha_modificacion,
                                ))
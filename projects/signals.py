from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Persona, Cliente
from django.db import transaction

@receiver(post_save, sender=Persona)
def create_cliente(sender, instance, created, **kwargs):
    if created:
        
        transaction.on_commit( lambda:Cliente.objects.create(
                                num_rut = instance,
                                p_nombre = instance.p_nombre,
                                s_nombre = instance.s_nombre,
                                p_apellido = instance.p_apellido,
                                s_apellido = instance.s_apellido,                                
                                fecha_nacimiento = instance.fecha_nacimiento,
                                telefono = instance.telefono,
                                email = instance.email,
                                direccion = instance.direccion,                                
                                fecha_creacion = instance.fecha_creacion,
                                ))
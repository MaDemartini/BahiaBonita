from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Persona, Cliente
from django.db import transaction

# al crear una persona, se crea un cliente automaticamente
# esto es para que no se repita el rut y el email en la base de datos, ya que son unicos


@receiver(post_save, sender=Persona)
def create_cliente(sender, instance, created, **kwargs):
    if created:
        def crear_cliente():
            try:
                Cliente.objects.create(
                    persona=instance,
                    fecha_creacion=instance.fecha_creacion,
                    fecha_modificacion=instance.fecha_modificacion,                    
                    fecha_eliminacion=instance.fecha_eliminacion
                )
                print("Cliente creado automáticamente desde signal.")
            except Exception as e:
                print(f"Error al crear cliente desde signal: {e}")

        transaction.on_commit(crear_cliente)
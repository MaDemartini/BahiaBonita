#registro personal del hotel
from projects.utils import email_personal, password_personal
from django.contrib.auth.hashers import make_password
from projects.models import Administrador, Persona, PersonalAseo, Recepcionista, Rol
from django.db import IntegrityError, transaction
from .correos_automaticos import correo_bienvenida_colab

@transaction.atomic #Así se evita que Persona se guarde si falla Administrador
def registrar_personal_hotel(datos, rol_nombre):
    try:
        rol = Rol.objects.get(nombre=rol_nombre)
    except Rol.DoesNotExist:
        raise ValueError(f"El rol {rol_nombre} no existe en la base de datos.")
    
    if not datos.get('nombre') or not datos.get('apellido'):
        raise ValueError("Nombre y Apellido son obligatorios.")

    # Crear la persona
    try:
        persona = Persona.objects.create(
            nombre=datos['nombre'],
            s_nombre=datos.get('s_nombre'),
            apellido=datos['apellido'],
            s_apellido=datos.get('s_apellido'),
            rut=datos.get('rut'),
            dv=datos.get('dv'),            
            fecha_nacimiento=datos['fecha_nacimiento'],
            direccion=datos.get('direccion'),
            pais=datos.get('pais'),
            ciudad=datos.get('ciudad'),
            telefono=datos.get('telefono'),
            rol=rol
        )
    except IntegrityError:
        raise ValueError("El email o RUT ya están registrados.")
    
    
    # generar email
    persona.email = email_personal(persona)    
    # Generar y guardar contraseña
    password_plana = password_personal(persona)
    persona.password = make_password(password_plana)
    
    persona.save()

    # Crear el registro en la tabla Administrador
    if rol.nombre == 'Administrador':        
        Administrador.objects.create(persona=persona)
        
    if rol.nombre == 'Recepcionista':
        Recepcionista.objects.create( persona=persona)
    
    if rol.nombre == 'Personal Aseo':
        PersonalAseo.objects.create(persona=persona)
        
    #datos para poder enviar el correo de bienvenida
    nombre = persona.nombre
    apellido = persona.apellido
    s_apellido = persona.s_apellido
    email = persona.email
    password = password_plana
    
    correo_bienvenida_colab (nombre, apellido, s_apellido, email, password)

    return persona, password_plana, persona.email #podemos inviar la pass por email o mostrarla en la interfaz de usuario
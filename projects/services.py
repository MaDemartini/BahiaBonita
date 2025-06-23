#registro personal del hotel
from projects.utils import password_personal
from django.contrib.auth.hashers import make_password
from projects.models import Administrador, Persona, Rol

def registrar_personal_hotel(datos, rol_nombre):
    try:
        rol = Rol.objects.get(nombre=rol_nombre)
    except Rol.DoesNotExist:
        raise ValueError(f"El rol {rol_nombre} no existe en la base de datos.")

    # Crear la persona
    persona = Persona.objects.create(
        nombre=datos['nombre'],
        s_nombre=datos.get('s_nombre'),
        apellido=datos['apellido'],
        s_apellido=datos.get('s_apellido'),
        rut=datos.get('rut'),
        dv=datos.get('dv'),
        email=datos['email'],
        fecha_nacimiento=datos['fecha_nacimiento'],
        direccion=datos.get('direccion'),
        pais=datos.get('pais'),
        ciudad=datos.get('ciudad'),
        telefono=datos.get('telefono'),
        rol=rol
    )

    # Generar y guardar contraseña
    password_plana = password_personal(persona)
    persona.password = make_password(password_plana)
    persona.save()

    # Crear el registro en la tabla Administrador
    if rol.nombre == 'Administrador':        
        Administrador.objects.create(
            persona=persona,
            fotoAdministrador=datos.get('fotoAdministrador'),
            profesión=datos.get('profesión'),
            cert_antecedentes=datos.get('cert_antecedentes'),
            tipo_prevision=datos.get('tipo_prevision'),
            sueldo=datos.get('sueldo')
        )

    return password_plana #podemos inviar la pass por email o mostrarla en la interfaz de usuario
from functools import wraps
from pyexpat.errors import messages
from django.shortcuts import redirect
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from django.conf import settings


def validar_dv(rut: str, dv: str) -> bool:
    rut = rut.strip()
    dv = dv.lower().strip()

    suma = 0
    multiplicador = 2

    for numero in reversed(rut):
        suma += int(numero) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2  
    
    resultado = 11 - (suma % 11)
    if resultado == 11:
        dv_esperado = '0'
    elif resultado == 10:
        dv_esperado = 'k'
    else:
        dv_esperado = str(resultado)

    return dv_esperado == dv.lower()

#############################################

# cracion de calendario para visualizar en panel de administracion en lista departamentos

from .models import Reserva

def resumen_calendar_deptos():
    reservas = Reserva.objects.all().values('departamento_id', 'fecha_ingreso', 'fecha_salida')
    fechas_reservadas = {}
    for r in reservas:
        depto_id = str(r['departamento_id'])
        if depto_id not in fechas_reservadas:
            fechas_reservadas[depto_id] = []
        fechas_reservadas[depto_id].append({
            'desde': r['fecha_ingreso'].isoformat(),
            'hasta': r['fecha_salida'].isoformat(),
        })
    return fechas_reservadas

#############################################

# Reutiliza verificar_token dentro del decorador para cerrar la sesion automaticamente si el token es inválido o ha expirado.
def verificar_token(request):
    token = request.session.get('jwt_token')
    if not token:
        return False
    try:
        jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return True
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return False

def verificar_sesion_jwt(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not verificar_token(request):
            request.session.flush()
            messages.error(request, "Tu sesión ha expirado o es inválida.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

#############################################
#creación de password para personal

def password_personal(persona):    
    iniciales = ''
    if persona.nombre:
        iniciales += persona.nombre[:2].upper()
    if persona.s_nombre:
        iniciales += persona.s_nombre[:2].upper()
    if persona.apellido:
        iniciales += persona.apellido[:2].upper()
    if persona.s_apellido:
        iniciales += persona.s_apellido[:2].upper()

    anno = str(persona.fecha_nacimiento.year)[:4] if persona.fecha_nacimiento else '00'
    correo = persona.email[:2].lower() if persona.email else 'xx'

    return f"{iniciales}{anno}{correo}"
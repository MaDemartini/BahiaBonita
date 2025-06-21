from django.conf import settings
import requests


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

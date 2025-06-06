from datetime import timedelta
from django.utils.timezone import now
from .models import Reserva

def eliminar_reservas_impagas():
    vencidas = Reserva.objects.filter(pagado=False, fecha_reserva__lt=now() - timedelta(minutes=10))
    cantidad = vencidas.count()
    vencidas.delete()
    print(f"Se eliminaron {cantidad} reservas no pagadas.")
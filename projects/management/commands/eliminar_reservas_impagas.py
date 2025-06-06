from django.core.management.base import BaseCommand
from projects.models import Reserva
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Elimina reservas no pagadas después de 10 minutos.'

    def handle(self, *args, **kwargs):
        limite = timezone.now() - timedelta(minutes=10)
        vencidas = Reserva.objects.filter(pagado=False, fecha_reserva__lt=limite)
        cantidad = vencidas.count()
        vencidas.delete()
        self.stdout.write(self.style.SUCCESS(f'Se eliminaron {cantidad} reservas no pagadas.'))
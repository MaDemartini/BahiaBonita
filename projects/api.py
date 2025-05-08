from .models import (Persona, Cliente, Administrador, PersonalAseo, Recepcionista, Departamento,
                     Reserva, CheckIn, Arriendo, TipoServicioAdicional,
                     ServicioAdicionalConsumido, Pago)

from rest_framework import viewsets, permissions
from .serializers import (PersonaSerializer, ClienteSerializer, AdministradorSerializer, PersonalAseoSerializer, RecepcionistaSerializer,
                          DepartamentoSerializer, ReservaSerializer,
                          CheckInSerializer, ArriendoSerializer, TipoServicioAdicionalSerializer,
                          ServicioAdicionalConsumidoSerializer, PagoSerializer)

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [permissions.AllowAny]

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.AllowAny]

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [permissions.AllowAny]

class PersonalAseoViewSet(viewsets.ModelViewSet):
    queryset = PersonalAseo.objects.all()
    serializer_class = PersonalAseoSerializer
    permission_classes = [permissions.AllowAny]

class RecepcionistaViewSet(viewsets.ModelViewSet):
    queryset = Recepcionista.objects.all()
    serializer_class = RecepcionistaSerializer
    permission_classes = [permissions.AllowAny]

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.AllowAny]

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [permissions.AllowAny]

class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [permissions.AllowAny]

class ArriendoViewSet(viewsets.ModelViewSet):
    queryset = Arriendo.objects.all()
    serializer_class = ArriendoSerializer
    permission_classes = [permissions.AllowAny]

class TipoServicioAdicionalViewSet(viewsets.ModelViewSet):
    queryset = TipoServicioAdicional.objects.all()
    serializer_class = TipoServicioAdicionalSerializer
    permission_classes = [permissions.AllowAny]

class ServicioAdicionalViewSet(viewsets.ModelViewSet):
    queryset = ServicioAdicionalConsumido.objects.all()
    serializer_class = ServicioAdicionalConsumidoSerializer
    permission_classes = [permissions.AllowAny]

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [permissions.AllowAny]

from .models import ( Persona,Cliente,Administrador,PersonalAseo,Recepcionista,Departamento,Reserva,
                     ReservaPresencial,ReservaOnline,CheckIn,Arriendo,TipoServicioAdicional,ServicioAdicional,DetalleServicios, Pago
)

from rest_framework import viewsets, permissions
from .serializers import (PersonaSerializer,ClienteSerializer,AdministradorSerializer,PersonalAseoSerializer,RecepcionistaSerializer,
                           DepartamentoSerializer,ReservaSerializer,ReservaPresencialSerializer,ReservaOnlineSerializer,
                           CheckInSerializer,ArriendoSerializer,TipoServicioAdicionalSerializer,ServicioAdicionalSerializer,
                           DetalleServiciosSerializer, PagoSerializer)

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer 
    lookup_field = 'num_rut' ##buscar por rut
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class AdministradorViewSet(viewsets.ModelViewSet):  
    queryset = Persona.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class PersonalAseoViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonalAseoSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class RecepcionistaViewSet(viewsets.ModelViewSet):          
    queryset = Persona.objects.all()
    serializer_class = RecepcionistaSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder 

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class ReservaPresencialViewSet(viewsets.ModelViewSet):
    queryset = ReservaPresencial.objects.all()
    serializer_class = ReservaPresencialSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class ReservaOnlineViewSet(viewsets.ModelViewSet):
    queryset = ReservaOnline.objects.all()
    serializer_class = ReservaOnlineSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class ArriendoViewSet(viewsets.ModelViewSet):
    queryset = Arriendo.objects.all()
    serializer_class = ArriendoSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class TipoServicioAdicionalViewSet(viewsets.ModelViewSet):
    queryset = TipoServicioAdicional.objects.all()
    serializer_class = TipoServicioAdicionalSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class ServicioAdicionalViewSet(viewsets.ModelViewSet):
    queryset = ServicioAdicional.objects.all()
    serializer_class = ServicioAdicionalSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

class DetalleServiciosViewSet(viewsets.ModelViewSet):
    queryset = DetalleServicios.objects.all()
    serializer_class = DetalleServiciosSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder
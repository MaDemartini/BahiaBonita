from .models import (Persona, Cliente, Administrador,PersonalAseo,Recepcionista,Departamento,
                     Reserva,CheckIn,Arriendo,TipoServicioAdicional,
                     ServicioAdicionalConsumido, Pago) 

from rest_framework import viewsets, permissions
from .serializers import (PersonaSerializer,ClienteSerializer,AdministradorSerializer,PersonalAseoSerializer,RecepcionistaSerializer,
                           DepartamentoSerializer,ReservaSerializer,
                           CheckInSerializer,ArriendoSerializer,TipoServicioAdicionalSerializer,
                           ServicioAdicionalConsumidoSerializer, PagoSerializer)

#sirve para el registro
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer     
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

#solo consulta de clientes registrados
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

#solo consulta de administradores registrados
class AdministradorViewSet(viewsets.ModelViewSet):  
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

#solo consulta de personal de aseo registrados
class PersonalAseoViewSet(viewsets.ModelViewSet):
    queryset = PersonalAseo.objects.all()
    serializer_class = PersonalAseoSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

#solo consulta de recepcionistas registrados
class RecepcionistaViewSet(viewsets.ModelViewSet):          
    queryset = Recepcionista.objects.all()
    serializer_class = RecepcionistaSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder

#creacion de departamentos y consulta de departamentos registrados
class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder 

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
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
    queryset = ServicioAdicionalConsumido.objects.all()
    serializer_class = ServicioAdicionalConsumidoSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder



class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [permissions.AllowAny]  ##todos pueden acceder
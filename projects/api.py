from .models import (Contacto, Persona, Cliente, Administrador, PersonalAseo, Recepcionista, Departamento,
                     Reserva, CheckIn, Arriendo, TipoServicioAdicional,
                     ServicioAdicionalConsumido, Pago)

from rest_framework import viewsets, permissions
from .serializers import (ContactoSerializer, PersonaSerializer, ClienteSerializer, AdministradorSerializer, PersonalAseoSerializer, RecepcionistaSerializer,
                          DepartamentoSerializer, ReservaSerializer,
                          CheckInSerializer, ArriendoSerializer, TipoServicioAdicionalSerializer,
                          ServicioAdicionalConsumidoSerializer, PagoSerializer)

from .serializers import DepartamentoInfoSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    filterset_fields = ['email']
    permission_classes = [permissions.AllowAny] #permite que todos accedan a la vista, en producción se debe de restringir el acceso

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

    @action(detail=False, methods=['get'], url_path='disponibles')
    def disponibles(self, request):
        # Filtra los departamentos que NO están en mantenimiento
        disponibles = Departamento.objects.filter(mantenimiento=False)
        serializer = DepartamentoInfoSerializer(disponibles, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='todos')
    def todos(self, request):
        # Obtiene todos los departamentos sin filtro
        departamentos = Departamento.objects.all()
        serializer = DepartamentoInfoSerializer(departamentos, many=True)
        return Response(serializer.data)

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
    
class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer
    permission_classes = [permissions.AllowAny]

    
    


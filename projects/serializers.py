from rest_framework import serializers
from .models import (Persona,Cliente,Administrador,PersonalAseo,Recepcionista, Departamento, 
               Reserva,  CheckIn, Arriendo, TipoServicioAdicional,
               ServicioAdicionalConsumido, Pago)     


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'fecha_eliminacion' ,)  # Solo lectura para el campo

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id_cliente','nombre','s_nombre','apellido','s_apellido','rut','fecha_nacimiento','direccion','telefono','email']

    

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'

class PersonalAseoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalAseo
        fields = '__all__'

class RecepcionistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recepcionista
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'

class ArriendoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arriendo
        fields = '__all__'

class TipoServicioAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicioAdicional
        fields = '__all__'

class ServicioAdicionalConsumidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioAdicionalConsumido
        fields = '__all__'



class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'



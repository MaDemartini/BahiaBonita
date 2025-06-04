from rest_framework import serializers
from .models import (Contacto, Persona, Cliente, Administrador, PersonalAseo, Recepcionista, Departamento,
                     Reserva, CheckIn, Arriendo, Rol, TipoServicioAdicional,
                     ServicioAdicionalConsumido, Pago)

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['id_persona', 'rol', 'nombre', 's_nombre', 'apellido', 's_apellido', 'rut',
                  'dv', 'fecha_nacimiento', 'direccion', 'telefono', 'email', 'password',
                  'fecha_creacion', 'fecha_modificacion', 'fecha_eliminacion']
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'fecha_eliminacion',)

class ClienteSerializer(serializers.ModelSerializer):
    id_persona = PersonaSerializer(read_only=True)
    class Meta:
        model = Cliente
        fields = ['id_persona','id_cliente', 'nombre', 's_nombre', 'apellido', 's_apellido', 'rut',
                  'fecha_nacimiento', 'direccion', 'telefono', 'email']

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

class DepartamentoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id_departamento', 'num_depto', 'cant_dormitorios', 'cant_banos',
                  'piso', 'cant_personas', 'valor_dia', 'imagen', 'mantenimiento']
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
        
class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = ['id_contacto','nombre', 'telefono', 'email', 'mensaje']
        read_only_fields = ('fecha_creacion',) 
        
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id_rol', 'nombre']
        read_only_fields = ('fecha_creacion', 'fecha_modificacion', 'fecha_eliminacion',)  # Assuming these fields exist in Rol model
        


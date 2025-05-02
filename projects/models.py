from django.conf import settings
from django.db import models
import uuid





# Create your models here.

class Persona(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )   
    num_rut = models.CharField(max_length=15, unique=True)
    p_nombre= models.CharField(max_length=15)
    s_nombre= models.CharField(max_length=15, blank=True)
    p_apellido= models.CharField(max_length=15)
    s_apellido= models.CharField(max_length=15, blank=True)
    fecha_nacimiento= models.DateField()
    direccion= models.CharField(max_length=100)
    telefono= models.CharField(max_length=15)
    email= models.EmailField(max_length=100, unique=True)
    password= models.CharField(max_length=100)
    re_password= models.CharField(max_length=100)
    fecha_creacion= models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = 'Persona'        
        ordering = 'num_rut','p_nombre', 's_nombre', 'p_apellido', 's_apellido'

    def __str__(self):
        return f'{self.num_rut}'
    

class Cliente(models.Model):
    id_cliente = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_rut = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='cliente')     
    p_nombre= models.CharField(max_length=15)
    s_nombre= models.CharField(max_length=15, blank=True)
    p_apellido= models.CharField(max_length=15)
    s_apellido= models.CharField(max_length=15, blank=True)
    fecha_nacimiento= models.DateField()
    direccion= models.CharField(max_length=100)
    telefono= models.CharField(max_length=15)
    email= models.EmailField(max_length=100, unique=True)
    fecha_creacion= models.DateTimeField(auto_now_add=True)    

    class Meta:
        verbose_name = 'Cliente' 
        ordering = ['num_rut','p_nombre', 's_nombre', 'p_apellido', 's_apellido']       
        

    def __str__(self):
        return f'{self.num_rut.num_rut}' 
    

class Administrador(models.Model):
    id_administrador = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_rut = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='administrador')
    

    class Meta:
        verbose_name = 'Administrador'        
        

    def __str__(self):
        return f'{self.num_rut.p_nombre} {self.num_rut.s_nombre} {self.num_rut.p_apellido} {self.num_rut.s_apellido} {self.num_rut.fecha_nacimiento} {self.num_rut.direccion} {self.num_rut.telefono} {self.num_rut.email} {self.num_rut.fecha_creacion} {self.num_rut.fecha_modificacion} {self.num_rut.fecha_eliminacion} {self.num_rut.estado}'


class PersonalAseo(models.Model):
    id_personal_aseo = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_rut = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='personal_aseo')
  
    class Meta:
        verbose_name = 'Personal Aseo'        
        

    def __str__(self):
        return f'{self.num_rut.p_nombre} {self.num_rut.s_nombre} {self.num_rut.p_apellido} {self.num_rut.s_apellido} {self.num_rut.fecha_nacimiento} {self.num_rut.direccion} {self.num_rut.telefono} {self.num_rut.email} {self.num_rut.estado}'


class Recepcionista(models.Model):
    id_recepcionista = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_rut = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='recepcionista')

    class Meta:
        verbose_name = 'Recepcionista'        
        

    def __str__(self):
        return f'{self.num_rut.p_nombre} {self.num_rut.s_nombre} {self.num_rut.p_apellido} {self.num_rut.s_apellido} {self.num_rut.fecha_nacimiento} {self.num_rut.direccion} {self.num_rut.telefono} {self.num_rut.email} {self.num_rut.estado}'


class Departamento(models.Model):
    id_depto = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_depto = models.IntegerField(3, unique=True)
    cant_dormitorios = models.IntegerField(2)
    cant_banos = models.IntegerField(2)
    piso = models.IntegerField(2)
    cant_personas = models.IntegerField(2)
    imagen = models.CharField(100)
    mantenimiento = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Departamento'        
        

    def __str__(self):
        return f'{self.num_depto} {self.cant_dormitorios} {self.cant_banos} {self.piso} {self.cant_personas} {self.imagen} {self.mantenimiento}'
    

class Reserva(models.Model):
    id_reserva = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_depto = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='reserva')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    valor = models.IntegerField(10)


    def __str__(self):
        return f'{self.id_depto.num_depto} {self.fecha_inicio} {self.fecha_fin} {self.valor}'
    

class ReservaPresencial(models.Model):
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='reservaPresencial')
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservaPresencial')
    id_recepcionista = models.ForeignKey(Recepcionista, on_delete=models.CASCADE, related_name='reservaPresencial')


    class Meta:
        verbose_name = 'Reserva Presencial'        
        ordering = ['id_cliente', 'id_reserva', 'id_recepcionista']

    def __str__(self):
                ##En este caso se retornan los datos indispensables del cliente##
        return (f'{self.id_cliente.num_rut.num_rut} {self.id_cliente.num_rut.p_nombre} {self.id_cliente.num_rut.s_nombre}'
                f'{self.id_cliente.num_rut.p_apellido} {self.id_cliente.num_rut.s_apellido}'
        
                 ##datos de la reserva##
                f'{self.id_reserva.id_depto.num_depto} {self.id_reserva.fecha_inicio} {self.id_reserva.fecha_fin} {self.id_reserva.valor}'

                ##datos del recepcionista##
                f'{self.id_recepcionista.num_rut.num_rut} {self.id_recepcionista.num_rut.p_nombre} {self.id_recepcionista.num_rut.p_apellido} {self.id_recepcionista.num_rut.s_apellido}'
                )
    
class ReservaOnline(models.Model):
    id_reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='reservaOnline', primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservaOnline')

    class Meta:
        verbose_name = 'Reserva Online'        
        ordering = ['id_cliente', 'id_reserva']

    def __str__(self):
                ##se retornan los datos del cliente##
        return (f'{self.id_cliente.num_rut.num_rut} {self.id_cliente.num_rut.p_nombre} {self.id_cliente.num_rut.s_nombre}'
                f'{self.id_cliente.num_rut.p_apellido} {self.id_cliente.num_rut.s_apellido} {self.id_cliente.num_rut.telefono} {self.id_cliente.num_rut.email}'
                
                ##datos reserva##
                f'{self.id_reserva.id_depto.num_depto} {self.id_reserva.fecha_inicio} {self.id_reserva.fecha_fin} {self.id_reserva.valor}'
                )
    
class CheckIn(models.Model):
    id_checkin = models.UUIDField(primary_key=True, editable=False)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='checkIn')
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='checkIn')  
    tipo_reserva = models.CharField(max_length=10, choices=[('presencial', 'Presencial'), ('online', 'Online')])  
    id_recepcionista = models.ForeignKey(Recepcionista, on_delete=models.CASCADE, related_name='checkIn')
    
    class Meta:
        verbose_name = 'Check In'        
        ordering = ['id_cliente', 'id_reserva', 'id_recepcionista']


    

    def __str__(self):
                ##En este caso se retornan los datos indispensables del cliente##
        return (f'{self.id_cliente.num_rut.num_rut} {self.id_cliente.num_rut.p_nombre} {self.id_cliente.num_rut.s_nombre}'
                f'{self.id_cliente.num_rut.p_apellido} {self.id_cliente.num_rut.s_apellido}'
                
                ##datos reserva ##
                f'{self.id_reserva.id_depto.num_depto} {self.id_reserva.fecha_inicio} {self.id_reserva.fecha_fin} {self.id_reserva.valor}'
                )
    
class Arriendo(models.Model):
    id_arriendo = models.UUIDField(primary_key=True, editable=False)
    id_checkin = models.ForeignKey(CheckIn, on_delete=models.CASCADE, related_name='arriendo')

    class Meta:
        verbose_name = 'Arriendo'        
        

    def __str__(self):
        return (f'{self.id_checkin.id_cliente.num_rut.num_rut} {self.id_checkin.id_cliente.num_rut.p_nombre} {self.id_checkin.id_cliente.num_rut.s_nombre} {self.id_checkin.id_cliente.num_rut.p_apellido} {self.id_checkin.id_cliente.num_rut.s_apellido}'
                f'{self.id_checkin.id_cliente.num_rut.telefono} {self.id_checkin.id_cliente.num_rut.email}'
                f'{self.id_checkin.id_reserva.id_depto.num_depto} {self.id_checkin.id_recepcionista.num_rut.num_rut}{self.id_checkin.id_recepcionista.num_rut.p_nombre}{self.id_checkin.id_recepcionista.num_rut.p_apellido} {self.id_checkin.id_recepcionista.num_rut.s_apellido}'

        )
    
class TipoServicioAdicional(models.Model):
    id_tipo_servicio = models.UUIDField(primary_key=True, editable=False)
    nombre_servicio = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, blank=True)
    valor_servicio = models.IntegerField(10)

    class Meta:
        verbose_name = 'Tipo Servicio Adicional'        
        

    def __str__(self):
        return f'{self.nombre_servicio} {self.descripcion} {self.valor_servicio}'
    
class ServicioAdicional(models.Model):
    id_servicio = models.UUIDField(primary_key=True, editable=False)
    id_tipo_servicio = models.ForeignKey(TipoServicioAdicional, on_delete=models.CASCADE, related_name='tipoServicioAdicional')
    cant_personas = models.IntegerField(2, blank=True)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    valor_servicio = models.IntegerField(10)

    class Meta:
        verbose_name = 'Servicio Adicional'        
        

    def __str__(self):
        return (f'{self.id_tipo_servicio.nombre_servicio} {self.id_tipo_servicio.descripcion} {self.id_tipo_servicio.valor_servicio} {self.cant_personas}'
                f'{self.hora_inicio} {self.hora_fin} {self.valor_servicio}'
        )
    
class DetalleServicios(models.Model):
    id_servicio_extra = models.UUIDField(primary_key=True, editable=False)
    id_arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE, related_name='detalleServicios')
    id_servicio_adicional = models.ForeignKey(ServicioAdicional, on_delete=models.CASCADE, related_name='detalleServicios')
    

    class Meta:
        verbose_name = 'Detalle Servicios'        
        

    def __str__(self):
        return (f'{self.id_arriendo.id_checkin.id_reserva.id_depto.num_depto} {self.id_arriendo.id_checkin.id_cliente.num_rut.num_rut}' 
                f'{self.id_arriendo.id_checkin.id_cliente.num_rut.p_nombre} {self.id_arriendo.id_checkin.id_cliente.num_rut.p_apellido}'
                f'{self.id_arriendo.id_checkin.id_cliente.num_rut.s_apellido}'
                
        )
    
class Pago(models.Model):
        id_pago = models.UUIDField(primary_key=True, editable=False)
        forma_de_pago = models.CharField(max_length=20, choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia')])
        id_arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE, related_name='pago')
        total_pago = models.IntegerField(10)
        fecha_pago = models.DateTimeField(auto_now_add=True)
        estado_pago = models.BooleanField(default=False)

        class Meta:
            verbose_name = 'Pago'
            
        def __str__(self):
            return (f'{self.id_arriendo.id_checkin.id_reserva.id_depto.num_depto} {self.id_arriendo.id_checkin.id_cliente.num_rut.num_rut}'
                    f'{self.id_arriendo.id_checkin.id_cliente.num_rut.p_nombre} {self.id_arriendo.id_checkin.id_cliente.num_rut.p_apellido}'
                    f'{self.id_arriendo.id_checkin.id_cliente.num_rut.s_apellido} {self.forma_de_pago} {self.total_pago} {self.fecha_pago} {self.estado_pago}'
            )
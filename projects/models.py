from django.db import models

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, unique=True)    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=20)
    s_nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    s_apellido = models.CharField(max_length=20)
    rut = models.CharField(max_length=12, unique=True)
    dv = models.CharField(max_length=1)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)    
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_eliminacion = models.DateTimeField(blank=True, null=True)    


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_eliminacion = models.DateTimeField(blank=True, null=True)

class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)    
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_eliminacion = models.DateTimeField(blank=True, null=True)

class PersonalAseo(models.Model):
    id_personal_aseo = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)    
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_eliminacion = models.DateTimeField(blank=True, null=True)

class Recepcionista(models.Model):
    id_recepcionista = models.AutoField(primary_key=True)    
    fecha_creacion = models.DateTimeField(auto_now=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_eliminacion = models.DateTimeField(blank=True, null=True)

class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    num_depto = models.IntegerField(unique=True)
    cant_dormitorios = models.IntegerField()
    cant_banos = models.IntegerField()
    piso = models.IntegerField()
    cant_personas = models.IntegerField()
    imagen = models.ImageField(blank=True, null=True)
    valor_dia = models.IntegerField()
    mantenimiento = models.BooleanField(default=False)

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    fecha_ingreso = models.DateField(blank=True)
    fecha_salida = models.DateField()
    cant_personas = models.IntegerField()
    valor_total = models.FloatField()
    tipo_reserva = models.CharField(max_length=20)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

class CheckIn(models.Model):
    id_checkin = models.AutoField(primary_key=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    recepcionista = models.ForeignKey(Recepcionista, on_delete=models.CASCADE)
    fecha_checkin = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Arriendo(models.Model):
    id_arriendo = models.AutoField(primary_key=True)
    checkIn = models.ForeignKey(CheckIn, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class TipoServicioAdicional(models.Model):
    id_tipo_servicio_adicional = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=100)
    valor = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

class ServicioAdicionalConsumido(models.Model):
    id_servicio_adicional_consumido = models.AutoField(primary_key=True)
    arreindo = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    tipo_servicio_adicional = models.ForeignKey(TipoServicioAdicional, on_delete=models.CASCADE)
    fecha_consumo = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    recepcionista = models.ForeignKey(Recepcionista, on_delete=models.CASCADE)
    fecha_pago = models.DateField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=20)
    valor_pago = models.IntegerField(10)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class view_resumen_reserva(models.Model):
    id_reserva = models.IntegerField()
    nombre_cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=10)
    departamento_numero = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cantidad_de_personas = models.IntegerField()
    tipo_de_reserva = models.CharField(max_length=20)
    total = models.FloatField()
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'view_resumen_reserva'
        
        
class Contacto(models.Model):
    id_contacto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    


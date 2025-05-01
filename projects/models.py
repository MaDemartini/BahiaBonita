from django.db import models



# Create your models here.

class Persona(models.Model):
    num_rut = models.UUIDField(primary_key=True, editable=False)
    p_nombre= models.CharField(max_length=15)
    s_nombre= models.CharField(max_length=15, blank=True)
    p_apellido= models.CharField(max_length=15)
    s_apellido= models.CharField(max_length=15, blank=True)
    fecha_nacimiento= models.DateField()
    direccion= models.CharField(max_length=100)
    telefono= models.CharField(max_length=15)
    email= models.EmailField(max_length=100, unique=True)

    fecha_creacion= models.DateTimeField(auto_now_add=True)
    fecha_modificacion= models.DateTimeField(auto_now=True)
    fecha_eliminacion= models.DateTimeField(null=True, blank=True)
    estado= models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Persona'        
        ordering = ['p_nombre', 's_nombre', 'p_apellido', 's_apellido']

    def __str__(self):
        return f'{self.p_nombre} {self.s_nombre} {self.p_apellido} {self.s_apellido}'
    

class cliente(models.Model):
    id_cliente = models.UUIDField(primary_key=True, editable=False)
    num_rut = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='cliente')
    

    class Meta:
        verbose_name = 'Cliente'        
        

    def __str__(self):
        return f'{self.num_rut.p_nombre} {self.num_rut.s_nombre} {self.num_rut.p_apellido} {self.num_rut.s_apellido} {self.num_rut.fecha_nacimiento} {self.num_rut.direccion} {self.num_rut.telefono} {self.num_rut.email} {self.num_rut.fecha_creacion} {self.num_rut.fecha_modificacion} {self.num_rut.fecha_eliminacion} {self.num_rut.estado}' 
    

class Administrador(models.Model):
    id_administrador = models.UUIDField(primary_key=True, editable=False)
    num_rut = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='administrador')
    

    class Meta:
        verbose_name = 'Administrador'        
        

    def __str__(self):
        return f'{self.num_rut.p_nombre} {self.num_rut.s_nombre} {self.num_rut.p_apellido} {self.num_rut.s_apellido} {self.num_rut.fecha_nacimiento} {self.num_rut.direccion} {self.num_rut.telefono} {self.num_rut.email} {self.num_rut.fecha_creacion} {self.num_rut.fecha_modificacion} {self.num_rut.fecha_eliminacion} {self.num_rut.estado}'


class personalAseo(models.Model):
    id_personal_aseo = models.UUIDField(primary_key=True, editable=False)
    num_rut = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='personal_aseo')
  
    class Meta:
        verbose_name = 'Personal Aseo'        
        

    def __str__(self):
        return f'{self.num_rut.p_nombre} {self.num_rut.s_nombre} {self.num_rut.p_apellido} {self.num_rut.s_apellido} {self.num_rut.fecha_nacimiento} {self.num_rut.direccion} {self.num_rut.telefono} {self.num_rut.email} {self.num_rut.estado}'


class recepcionista(models.Model):
    id_recepcionista = models.UUIDField(primary_key=True, editable=False)
    num_rut = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='recepcionista')

    class Meta:
        verbose_name = 'Recepcionista'        
        

    def __str__(self):
        return f'{self.num_rut.p_nombre} {self.num_rut.s_nombre} {self.num_rut.p_apellido} {self.num_rut.s_apellido} {self.num_rut.fecha_nacimiento} {self.num_rut.direccion} {self.num_rut.telefono} {self.num_rut.email} {self.num_rut.estado}'


class Departamento(models.Model):
    id_depto = models.UUIDField(primary_key=True, editable=False)
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
    

class reserva(models.Model):
    id_reserva = models.UUIDField(primary_key=True, editable=False)
    id_depto = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='reserva')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    valor = models.IntegerField(10)


    def __str__(self):
        return f'{self.id_depto.num_depto} {self.fecha_inicio} {self.fecha_fin} {self.valor}'
    

class reservaPresencial(models.Model):
    id_reserva = models.ForeignKey(reserva, on_delete=models.CASCADE, related_name='reservaPresencial')
    id_cliente = models.ForeignKey(cliente, on_delete=models.CASCADE, related_name='reservaPresencial')
    id_recepcionista = models.ForeignKey(recepcionista, on_delete=models.CASCADE, related_name='reservaPresencial')

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
    

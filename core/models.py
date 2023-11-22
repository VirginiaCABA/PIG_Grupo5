from django.db import models
from django.urls import reverse_lazy
from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.utils import timezone

# Create your models here.

class Provincia(models.Model):
    idprovincia = models.AutoField(primary_key=True),
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    baja = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre}"

    def soft_delete(self):
        self.baja = True
        super().save()

    def restore(self):
        self.baja = False
        super().save()

class Localidad(models.Model):
    idlocalidad = models.AutoField(primary_key=True),
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)  # relacion muchos a uno
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    baja = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre}"

    def soft_delete(self):
        self.baja = True
        super().save()

    def restore(self):
        self.baja = False
        super().save()

    class Meta():
        verbose_name_plural = 'Localidades'

class Domicilio(models.Model):
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)  # relacion muchos a uno
    calle = models.CharField(max_length=150, verbose_name='Calle')
    numero = models.IntegerField(verbose_name="Número")
    piso = models.IntegerField(verbose_name="Piso")
    departamento = models.CharField(max_length=150, verbose_name='Dpto')
    cp = models.IntegerField(verbose_name="Código Postal")
    latitud = models.FloatField(verbose_name="Latitud")
    longitud = models.FloatField(verbose_name="Longitud")
    baja = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f"Provincia: {self.localidad.provincia.nombre}, Localidad: {self.localidad.nombre}, CP: {self.cp}, Calle: {self.calle}, Numero: {self.numero} "
    
    def soft_delete(self):
        self.baja = True
        super().save()

    def restore(self):
        self.baja = False
        super().save()
    
    class Meta():
        verbose_name_plural = 'Domicilios'

class EstadoPedido(models.TextChoices): #Estado de Pedido
    RECIBIDO = '1', 'Recibido'
    PROCESADO = '2', 'Procesado'
    ASIGNADO = '3', 'Asignado'
    ENTREGADO = '4', 'Entregado'
    NO_ENTREGADO_VISITA1 = '5','No entregado en 1er visita'
    NO_ENTREGADO_VISITA2 = '6','No entregado en 2da visita'


class Sucursal(models.Model):
    idsucursal =  models.AutoField(primary_key=True),
    domicilio = models.ForeignKey(Domicilio, on_delete=models.CASCADE)  # relacion muchos a uno
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    numero = models.IntegerField(verbose_name="Número")

    def __str__(self):
        return f"{self.nombre} - {self.numero}"

    class Meta():
        verbose_name_plural = 'Sucursales'

class Persona(User):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=150, verbose_name='Apellido')
    mail = models.EmailField(max_length=150, null=True)
    baja = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    def soft_delete(self):
        self.baja = True
        super().save()

    def restore(self):
        self.baja = False
        super().save()

    class Meta:
        abstract = True
    
class PostulanteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(baja=False)
    
class Postulante(Persona):
    idpostulante = models.AutoField(primary_key=True),
    dni =  models.CharField(verbose_name="DNI",
                            max_length=10,
                            validators=[RegexValidator(r'^\d{8,10}$',
                            message='El número de dni debe tener entre 8 y 10 dígitos.')])
    curriculum = models.FileField(upload_to='cv_upload/')
    mensaje = models.TextField(max_length=500, blank=True, null=True)
    objects = PostulanteManager()

    def __str__(self):
        return f"{self.dni} - " + super().__str__()
    
    def save(self, *args, **kwargs):
        self.username = self.dni
        self.password = self.dni
        super(Postulante, self).save(*args, **kwargs)

    def obtener_baja_url(self):
        return reverse_lazy('postulante_baja', args=[self.idpostulante])

    def obtener_modificacion_url(self):
        return reverse_lazy('postulante_modificacion', args=[self.idpostulante])

    class Meta():
        verbose_name_plural = 'Postulantes'

""" class ClienteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(baja=False) """
    
class Cliente(Persona):
    idcliente = models.AutoField(primary_key=True),
    cuit = models.BigIntegerField(verbose_name="CUIT")
    domicilio = models.ForeignKey(Domicilio, on_delete=models.CASCADE)  # relacion muchos a uno
    #objects = ClienteManager()

    def __str__(self):
        return f"{self.cuit} - " + super().__str__()

    def obtener_baja_url(self):
        return reverse_lazy('cliente_baja', args=[self.idcliente])

    def obtener_modificacion_url(self):
        return reverse_lazy('cliente_modificacion', args=[self.idcliente])

    class Meta():
        verbose_name_plural = 'Clientes'

def add_cliente_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='cliente'))

post_save.connect(add_cliente_group, sender=Cliente)

class Pedido(models.Model):
    idpedido = models.AutoField(primary_key=True)
    domicilio = models.ForeignKey(Domicilio, on_delete=models.CASCADE)  # relacion muchos a uno
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # relacion muchos a uno
    estado = models.CharField(max_length=3, choices=EstadoPedido.choices, default=EstadoPedido.RECIBIDO)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.idpedido} - {self.domicilio} - {self.fecha_creacion}"

    def get_estado(self):
        return dict(EstadoPedido.choices)[self.estado]


class Paquete(models.Model):
    idpaquete = models.AutoField(primary_key=True),
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # relacion muchos a uno
    peso = models.FloatField(verbose_name="Peso")
    ancho = models.FloatField(verbose_name="Ancho")
    largo = models.FloatField(verbose_name="Largo")
    alto = models.FloatField(verbose_name="Alto")
    objects = models.Manager()

    def to_dict(self):
        return {
            'peso': str(self.peso),
            'ancho': str(self.ancho),
            'largo': str(self.largo),
            'alto': str(self.alto),
        }


""" class EmpleadoManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(baja=False) """
    
class Empleado(models.Model):
    idempleado = models.AutoField(primary_key=True),
    postulante = models.OneToOneField(Postulante, on_delete=models.CASCADE, unique=False)
    pedidos = models.ManyToManyField(Pedido, through='AsignacionPedido') # relacion muchos a muchos
    #baja = models.BooleanField(default=False)
    #objects = EmpleadoManager()

    def __str__(self):
        return f"{self.postulante.__str__()}"

    def obtener_baja_url(self):
        return reverse_lazy('empleado_baja', args=[self.idempleado])

    def obtener_modificacion_url(self):
        return reverse_lazy('empleado_modificacion', args=[self.idempleado])

    class Meta():
        verbose_name_plural = 'Empleados'

def add_empleado_group(sender, instance, created, **kwargs):
    if created:
        instance.postulante.groups.add(Group.objects.get(name='empleado'))

post_save.connect(add_empleado_group, sender=Empleado)

class AsignacionPedido(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.empleado.__str__()} - {self.pedido.__str__()}"
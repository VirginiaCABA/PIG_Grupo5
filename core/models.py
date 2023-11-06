from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.core.validators import RegexValidator

# Create your models here.
class Domicilio(models.Model):
    iddomicilio = models.AutoField(primary_key=True),
    calle = models.CharField(max_length=150, verbose_name='Calle')
    numero = models.IntegerField(verbose_name="Número")
    cp = models.IntegerField(verbose_name="Código Postal")
    piso = models.IntegerField(verbose_name="Piso")
    departamento = models.CharField(max_length=150, verbose_name='Dpto')
    latitud = models.FloatField(verbose_name="Latitud")
    longitud = models.FloatField(verbose_name="Longitud")
    objects = models.Manager()

    def __str__(self):
        return f"{self.calle}, {self.numero}"

class EstadoPedido(models.TextChoices): #Estado de Pedido
    RECIBIDO = '1', 'Recibido'
    PROCESADO = '2', 'Procesado'
    ASIGNADO = '3', 'Asignado'
    ENTREGADO = '4', 'Entregado'
    NO_ENTREGADO_VISITA1 = '5','No entregado en 1er visita'
    NO_ENTREGADO_VISITA2 = '6','No entregado en 2da visita'

class Pedido(models.Model):
    idpedido = models.AutoField(primary_key=True),
    estado = models.CharField(max_length=3, choices=EstadoPedido.choices, default=EstadoPedido.RECIBIDO)
    domicilio_destino = models.ForeignKey(Domicilio, on_delete=models.CASCADE)  # relacion muchos a uno

class Paquete(models.Model):
    idpaquete = models.AutoField(primary_key=True),
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # relacion muchos a uno
    peso = models.FloatField(verbose_name="Peso")
    ancho = models.FloatField(verbose_name="Ancho")
    largo = models.FloatField(verbose_name="Largo")
    alto = models.FloatField(verbose_name="Alto")
    objects = models.Manager()

class Sucursal(models.Model):
    idsucursal =  models.AutoField(primary_key=True),
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    numero = models.IntegerField(verbose_name="Número")
    domicilio = models.ForeignKey(Domicilio, on_delete=models.CASCADE)  # relacion muchos a uno

class Persona(models.Model):
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

    def obtener_baja_url(self):
        return reverse_lazy('postulante_baja', args=[self.idpostulante])

    def obtener_modificacion_url(self):
        return reverse_lazy('postulante_modificacion', args=[self.idpostulante])

    class Meta():
        verbose_name_plural = 'Postulantes'

class EmpleadoManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(baja=False)

class Empleado(Postulante):
    idempleado = models.AutoField(primary_key=True),
    pedidos = models.ManyToManyField(Pedido, through='AsignacionPedido') # relacion muchos a muchos
    objects = EmpleadoManager()

    def __str__(self):
        return f"{self.dni} - " + super().__str__()

    def obtener_baja_url(self):
        return reverse_lazy('empleado_baja', args=[self.idempleado])

    def obtener_modificacion_url(self):
        return reverse_lazy('empleado_modificacion', args=[self.idempleado])

    class Meta():
        verbose_name_plural = 'Empleados'

class AsignacionPedido(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha = models.DateField()

class ClienteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(baja=False)
    
class Cliente(Persona):
    idcliente = models.AutoField(primary_key=True),
    cuit = models.IntegerField(verbose_name="CUIT")
    domicilio = models.ForeignKey(Domicilio, on_delete=models.CASCADE)  # relacion muchos a uno
    objects = ClienteManager()

    def __str__(self):
        return f"{self.cuit} - " + super().__str__()

    def obtener_baja_url(self):
        return reverse_lazy('cliente_baja', args=[self.idcliente])

    def obtener_modificacion_url(self):
        return reverse_lazy('cliente_modificacion', args=[self.idcliente])

    class Meta():
        verbose_name_plural = 'Clientes'


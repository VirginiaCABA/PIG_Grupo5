from django.contrib import admin
from .models import Domicilio, Sucursal, Cliente, Empleado, AsignacionPedido
# Register your models here.
admin.site.register([Domicilio,
                     Sucursal,
                     Cliente,
                     Empleado,
                     AsignacionPedido])
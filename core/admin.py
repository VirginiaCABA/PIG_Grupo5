from django.contrib import admin
from .models import AsignacionPedido, Cliente, Persona, Domicilio, Empleado
# Register your models here.
admin.site.register(AsignacionPedido)
admin.site.register(Cliente)
admin.site.register(Persona)
admin.site.register(Domicilio)
admin.site.register(Empleado)

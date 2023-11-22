from django.contrib import admin
from .models import Provincia, Localidad, Domicilio, Sucursal, Cliente, Empleado, AsignacionPedido

class CustomAdmin(admin.AdminSite):
    site_header = 'Administración de Logistica'
    site_title = 'Sitio de Administración'
    index_title = 'Administrador del Sitio'

    def has_permission(self, request):
        return request.user.is_authenticated and (request.user.groups.filter(name='administrador').exists() or request.user.is_superuser)

admin_custom = CustomAdmin(name = 'LogisticaAdmin')

# Register your models here.
admin_custom.register([Provincia, Localidad, Domicilio, Sucursal, Empleado])


class ClienteAdmin(admin.ModelAdmin):
    fields = ["username", "password", "nombre", "apellido", "mail", "cuit", "domicilio"]

admin_custom.register(Cliente, ClienteAdmin)

class AsignacionPedidoAdmin(admin.ModelAdmin):
    fields = ["empleado", "pedido"]

admin_custom.register(AsignacionPedido, AsignacionPedidoAdmin)

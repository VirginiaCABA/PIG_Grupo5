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

class ProvinciaAdmin(admin.ModelAdmin):
    exclude = ['baja']

admin_custom.register(Provincia, ProvinciaAdmin)

class LocalidadAdmin(admin.ModelAdmin):
    exclude = ['baja']

admin_custom.register(Localidad, LocalidadAdmin)

class DomicilioAdmin(admin.ModelAdmin):
    exclude = ['baja']

admin_custom.register(Domicilio, DomicilioAdmin)

class SucursalAdmin(admin.ModelAdmin):
    exclude = ['baja']

admin_custom.register(Sucursal, SucursalAdmin)

class EmpleadoAdmin(admin.ModelAdmin):
    exclude = ['baja']

admin_custom.register(Empleado, EmpleadoAdmin)

class ClienteAdmin(admin.ModelAdmin):
    fields = ["username", "password", "nombre", "apellido", "mail", "cuit", "domicilio"]

admin_custom.register(Cliente, ClienteAdmin)

class AsignacionPedidoAdmin(admin.ModelAdmin):
    fields = ["empleado", "pedido"]

admin_custom.register(AsignacionPedido, AsignacionPedidoAdmin)

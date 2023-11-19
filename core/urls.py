"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
# from core.admin import admin_custom
from core.views import *
from django.contrib import admin


urlpatterns = [
    path('', home, name='home'),
    # path('administracion/', admin_custom.urls),
    path('administracion/', admin.site.urls, name='admin'),
    path('nosotros/', nosotros, name='nosotros'),
    path('servicios/', servicios, name='servicios'),
    path('contacto/', contacto, name='contacto'),
    path('clientes/', PedidosView.as_view(), name='clientes'),
    path('registrar_pedido/', PedidosCreateView.as_view(), name='registrar_pedido'),
    path('registrar_domicilio/', DomicilioCreateView.as_view(), name='registrar_domicilio'),
    path('registrar_cliente/', ClienteCreateView.as_view(), name='registrar_cliente'),
    re_path(r'^empleados/(?P<fecha>\d{4}-\d{2}-\d{2})/$',  empleados, name='empleados'),
    path('logout/', exit, name='exit'),
]

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
from core.views import *

urlpatterns = [
    path('', home, name='home'),
    path('nosotros/', nosotros, name='nosotros'),
    path('servicios/', servicios, name='servicios'),
    path('contacto/', contacto, name='contacto'),
    path('clientes/', clientes, name='clientes'),
    re_path(r'^empleados/(?P<fecha>\d{4}-\d{2}-\d{2})/$',  empleados, name='empleados'),
    path('logout/', exit, name='exit'),
    path('crear_pedido/', crear_pedido, name='crear_pedido'),
]

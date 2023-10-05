from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from .forms import CreateCostumerForm

# Create your views here.

def home(request):
    '''Devuelve la vista principal del sitio.'''
    return render(request ,"core/pages/home.html")

def nosotros(request):
    '''Devuelve la section de nosotros.'''
    return render(request ,"core/pages/nosotros.html")

def servicios(request):
    '''Devuelve la section de servicios.'''
    return render(request ,"core/pages/servicios.html")

def contacto(request):
    '''Devuelve la section de contacto.'''
    return render(request ,"core/pages/contacto.html")

@login_required
def clientes(request):
    '''Recibe los datos del usuario y devuelve la vista de clientes.'''
    return render(request ,"core/pages/clientes.html")

@login_required
def empleados(request, fecha):
    '''Recibe los datos del usuario y devuelve la vista de empleados.'''
    pedidos = {
        'headers' : 
            [ 'Fecha pedido', 'Descripción', 'Lugar de Entrega' ],
        'rows' : 
            [
                [ '2012-09-14 14:23', 'Cosa 1', 'Rivadavia 1245' ],
                [ '2012-09-14 16:51', 'Cosa 2', 'San Martín 3200' ]
            ]
    }
    return render(request ,"core/pages/empleados.html", { 'fecha' : fecha, 'pedidos': pedidos })

def exit(request):
    '''Cierre la sesión y envía al home'''
    logout(request)
    return redirect('home')

def crear_pedido(request):
    if (request.method == 'POST'):
        form = CreateCostumerForm(request.POST)
        if form.is_valid():
            servicios = form.cleaned_data['servicios']
            
            # return render(request, 'success.html')
    else:
        form = CreateCostumerForm()
    return render(request,"core/crear_pedido.html", {'form': form})

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import PedidoForm, ContactoForm

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
    formulario = None
    error = None
    if request.method == 'GET':
        formulario = ContactoForm()
    elif request.method == "POST":
        formulario = ContactoForm(request.POST, request.FILES)
        if formulario.is_valid():
            #Si los datos son válidos, los captura en variables
            nombre = formulario.cleaned_data['nombre']
            apellido = formulario.cleaned_data['apellido']
            dni = formulario.cleaned_data['dni']
            mail = formulario.cleaned_data['mail']
            mensaje = formulario.cleaned_data['mensaje']
            curriculum = request.FILES['curriculum']

            #formatear mensaje de respuesta
            mensaje_html = f'Mensaje de contacto de {nombre} {apellido} (DNI: {dni}):\n {mensaje}'

            #Y finalmente, se envía el mail
            email = EmailMessage(
                "Recibimos tus datos",
                mensaje_html,
                settings.EMAIL_HOST_USER,
                [mail],  # Lista de destinatarios
            )
            email.attach(curriculum.name,
                         curriculum.read(),
                         curriculum.content_type)
            email.send()
            
            return HttpResponse('Correo enviado con éxito') #ver si cambio a ResponseRedirect
        else:
            error = HttpResponseBadRequest("Datos inválidos.")
    else:
        error = HttpResponseBadRequest("No tiene permiso para el método utilizado.")
    context = {
        'contacto_form' : formulario      
    }
    return render(request ,"core/pages/contacto.html" , context) if error is None else error

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
        form = PedidoForm(request.POST)
        if form.is_valid():
            servicios = form.cleaned_data['servicios']
            # return render(request, 'success.html')
    else:
        form = PedidoForm()
    return render(request,"core/crear_pedido.html", {'form': form})

def contac_bas(request):
        if request.method == 'POST':
            form = ContactoForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['nombre']
            lastname = form.cleaned_data['apellido']
            dni =  form.cleaned_data['dni']
            mail = form.cleaned_data['mail']
            mensaje = form.cleaned_data['mensaje']
            
            return redirect('contacto')
        else:
            form = ContactoForm()
        return render (request, 'contacto.html',{'form':form})
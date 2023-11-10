from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from .models import Postulante
from .forms import ContactoForm, PedidoForm, ClienteForm, DomicilioForm

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
    respuesta = None
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
            #verificar que no existe el mail en la BD
            if Postulante.objects.filter(mail=mail).exists():
                respuesta = HttpResponseBadRequest(f"El Email {mail} ya esta registrado.")
            else:
                #guardar los datos en la BD
                nuevo_postulante = Postulante(nombre=nombre, apellido=apellido, dni=dni,
                                        mail=mail, mensaje=mensaje, curriculum=curriculum)
                nuevo_postulante.save()
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
                respuesta = HttpResponseRedirect("core/pages/mensaje_envio.html")
        else:
            respuesta = HttpResponseBadRequest("Datos inválidos.") 
    else:
        respuesta = HttpResponseBadRequest("No tiene permiso para el método utilizado.")
    context = {
        'contacto_form' : formulario      
    }
    return render(request ,"core/pages/contacto.html" , context) if respuesta is None else respuesta

@login_required
def clientes(request):
    '''Recibe los datos del usuario y devuelve la vista de clientes.'''
    pedidos = {
        'headers' : 
            [ 'Fecha pedido', 'Descripción', 'Lugar de Entrega' ],
        'rows' : 
            [
                [ '2012-09-14 14:23', 'Cosa 1', 'Rivadavia 1245' ],
                [ '2012-09-14 16:51', 'Cosa 2', 'San Martín 3200' ]
            ]
    }
    return render(request ,"core/pages/clientes.html", { 'pedidos': pedidos })


class ClienteCreateView(CreateView):
    '''Devuelve el formulario de registro del nuevo cliente'''
    template_name = 'core/pages/registrar_cliente.html'
    form_class = ClienteForm
    second_form_class = DomicilioForm
    success_url = '/login/'

    def post(self, request, *args, **kwargs):
        cliente = self.form_class(request.POST)
        domicilio = self.second_form_class(request.POST, prefix='domicilio')
        
        if domicilio.is_valid():
            domicilio = domicilio.save(commit=False)
            domicilio.save()
            if cliente.is_valid():
                cliente.domicilio = domicilio
                cliente.save()
            return redirect(self.request.path)

class PedidoCreateView(LoginRequiredMixin, CreateView):
    '''Devuelve el formulario de solicitud de envío'''
    template_name = 'core/pages/registrar_pedido.html'
    form_class = PedidoForm
    success_url = '/clientes/'

    def form_valid(self, form):
        return super().form_valid(form)

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

from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Postulante, Paquete, Domicilio, Cliente
from .forms import ContactoForm, PedidoForm, PaqueteFormSet, DomicilioFormSet, ClienteForm
from django.contrib import messages


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

def registrocliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password == password2:
                # Controla si el usuario ya existe
                if Cliente.objects.filter(mail=mail).exists():
                    messages.error(request, 'Este cliente ya existe.')
                    messages.info(request, 'Este cliente ya existe INFO.')
                    # return redirect('login')
                else:
                    # Crea el usuario
                    form.save()
                    messages.success(request, 'Cliente registrado exitosamente.')
                    return redirect('login')  # Redirecciona a otra pàagina una vez que se registra
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
    else:
        form = ClienteForm()
    return render(request,"core/pages/registro_cliente.html", {'form': form})


@login_required
def clientes(request):
    '''Recibe los datos del usuario y devuelve la vista de clientes.'''
    if (request.method == 'POST'):
        
        pedido_form = PedidoForm(request.POST)
        domicilio_formset = DomicilioFormSet(request.POST, prefix='domicilios', queryset=Domicilio.objects.none())
        paquete_formset = PaqueteFormSet(request.POST, prefix='paquetes', queryset=Paquete.objects.none())

        if pedido_form.is_valid():
            pedido = pedido_form.save()
            
            """ if domicilio_formset.is_valid():
                domicilio_formset.save(commit=False)
                for form in domicilio_formset.forms:
                    domicilio = form.save(commit=False)
                    domicilio.pedido = pedido
                    domicilio.save() """

            if paquete_formset.is_valid():
                paquete_formset.save(commit=False)
                for form in paquete_formset.forms:
                    paquete = form.save(commit=False)
                    paquete.pedido = pedido
                    paquete.save()

            return HttpResponse('Pedido cargado')
    else:
        pedido_form = PedidoForm()
        domicilio_formset = DomicilioFormSet(queryset=Domicilio.objects.none(), prefix='domicilio')
        paquete_formset = PaqueteFormSet(queryset=Paquete.objects.none(), prefix='paquetes')

    return render(request ,"core/pages/clientes.html", {
        'pedido_form': pedido_form,
        'domicilio_formset': domicilio_formset,
        'paquete_formset': paquete_formset
        })

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

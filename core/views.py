from django.conf import settings
from django.http import HttpResponseBadRequest
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from .models import Postulante, Paquete, Pedido, EstadoPedido, Empleado, Localidad, Provincia, Domicilio
from .forms import ContactoForm, PedidoForm, ClienteForm, PaqueteForm
from django.views.generic import ListView, CreateView
#from django.urls import reverse
from django.shortcuts import render


def admin(request):
    return redirect('admin')

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
                # respuesta = HttpResponseRedirect("/core/pages/mensaje_envio.html")
                return redirect('contacto')
        else:
            respuesta = HttpResponseBadRequest("Datos inválidos.") 
    else:
        respuesta = HttpResponseBadRequest("No tiene permiso para el método utilizado.")
    context = {
        'contacto_form' : formulario      
    }
    return render(request ,"core/pages/contacto.html" , context) if respuesta is None else respuesta


class PedidosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Paquete
    template_name = 'core/pages/clientes.html'
    ordering = ['id']

    def test_func(self):
        return self.request.user.groups.filter(name='cliente').exists()
        
    def get_queryset(self):
        queryset = Paquete.objects.filter(pedido__cliente=self.request.user.id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Pedidos"
        context['headers'] = [ 'Id Pedido', 'Id Paquete', 'Fecha pedido', 'Descripción', 'Lugar de Entrega', 'Estado' ]
        # context['url_alta'] = reverse_lazy('estudiante_alta')
        return context
    
class PedidosCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Paquete
    form_class = PaqueteForm
    template_name = 'core/pages/nuevoPedido.html'
    
    def test_func(self):
        return self.request.user.groups.filter(name='cliente').exists()
    
    def form_valid(self, form):
        submit_type = self.request.POST.get('submit_pedido') 
        submit_type = self.request.POST.get('submit_type')
        paquete = form.save(commit=False)
        paquetes = self.request.session.get('paquetes', [])
        paquetes.append(paquete.to_dict())
        if submit_type == 'Guardar':
            context = self.get_context_data()
            self.request.session['paquetes'] = paquetes
            context['paquetes'] = paquetes
            context['inicio'] = False
            context['titulo'] = "Nuevo Pedido"
            return render(self.request, self.template_name, context)
        else:
            nuevo_formulario = PaqueteForm()
            context = self.get_context_data()
            self.request.session['paquetes'] = paquetes
            context['paquetes'] = paquetes
            context['form'] = nuevo_formulario
        return render(self.request, self.template_name, context)
     
    def form_invalid(self, form):
        # errores=form.errors
        paquetes = self.request.session.get('paquetes', [])
        submit_paquete = self.request.POST.get('submit_paquete')
        submit_pedido = self.request.POST.get('submit_pedido') 
        del_paquete = self.request.POST.get('del_paquete') 
        if not del_paquete == None:
            paquetes = self.request.session.get('paquetes', [])
            n = int(del_paquete) - 1
            del paquetes[n]
            # nuevo_formulario = PaqueteForm()
            context = self.get_context_data()
            self.request.session['paquetes'] = paquetes
            context['paquetes'] = paquetes
            # context['form'] = nuevo_formulario
            return render(self.request, self.template_name, context)
        if submit_pedido == 'Guardar':
            pedido_form = PedidoForm(self.request.POST)
            if pedido_form.is_valid():
                if Provincia.objects.filter(nombre__icontains=pedido_form.cleaned_data['provincia']).exists():
                    provincia_id= Provincia.objects.filter(nombre__icontains=pedido_form.cleaned_data['provincia'])[0].id
                else:
                    provincia=Provincia(nombre=pedido_form.cleaned_data['provincia'],baja=False)
                    provincia.save()
                    provincia_id = provincia.id

                if Localidad.objects.filter(nombre__icontains=pedido_form.cleaned_data['localidad'], provincia_id=provincia_id ).exists():
                    localidad_id= Localidad.objects.filter(nombre__icontains=pedido_form.cleaned_data['localidad'], provincia_id=provincia_id)[0].id
                else:
                    localidad=Localidad(nombre=pedido_form.cleaned_data['localidad'],baja=False,provincia_id=provincia_id)
                    localidad.save()
                    localidad_id = localidad.id

                if Domicilio.objects.filter(calle__icontains=pedido_form.cleaned_data['calle'],
                                            numero__icontains=pedido_form.cleaned_data['numero'],
                                            piso__icontains=pedido_form.cleaned_data['piso'],
                                            departamento__icontains=pedido_form.cleaned_data['departamento'],
                                            cp__icontains=pedido_form.cleaned_data['cp'],
                                            latitud__icontains=pedido_form.cleaned_data['latitud'],
                                            longitud__icontains=pedido_form.cleaned_data['longitud'],
                                            localidad_id=localidad_id).exists():
                    domicilio_id= Domicilio.objects.filter(calle__icontains=pedido_form.cleaned_data['calle'],
                                                           numero__icontains=pedido_form.cleaned_data['numero'],
                                                           piso__icontains=pedido_form.cleaned_data['piso'],
                                                           departamento__icontains=pedido_form.cleaned_data['departamento'],
                                                           cp__icontains=pedido_form.cleaned_data['cp'],
                                                           latitud__icontains=pedido_form.cleaned_data['latitud'],
                                                           longitud__icontains=pedido_form.cleaned_data['longitud'],
                                                           localidad_id=localidad_id)[0].id
                else:
                    domicilio=Domicilio(calle=pedido_form.cleaned_data['calle'],
                                        numero=pedido_form.cleaned_data['numero'],
                                        piso=pedido_form.cleaned_data['piso'],
                                        departamento=pedido_form.cleaned_data['departamento'],
                                        cp=pedido_form.cleaned_data['cp'],
                                        latitud=pedido_form.cleaned_data['latitud'],
                                        longitud=pedido_form.cleaned_data['longitud'],
                                        baja=False,
                                        localidad_id=localidad_id)
                    domicilio.save()
                    domicilio_id = domicilio.id   
                # pedido = Pedido(estado=EstadoPedido.RECIBIDO.value,domicilio_id=pedido_form.cleaned_data['domicilio'].id, cliente_id=self.request.user.id)
                pedido = Pedido(estado=EstadoPedido.RECIBIDO.value,domicilio_id=domicilio_id, cliente_id=self.request.user.id)
                pedido.save()
                paquetes = self.request.session.get('paquetes', [])
                for paquete_data in paquetes:
                    paquete_data['pedido_id'] = pedido.idpedido

                paquetes_objects = [Paquete(**data) for data in paquetes]
                Paquete.objects.bulk_create(paquetes_objects)
                self.request.session['paquetes'] = []
                return redirect('clientes')
        if submit_paquete == 'Guardar':
            paquetes = self.request.session.get('paquetes', [])
            context = self.get_context_data()
            self.request.session['paquetes'] = paquetes
            context['paquetes'] = paquetes
            context['headers'] = [ 'Paquete', 'Peso', 'Ancho', 'Largo', 'Alto']
            context['inicio'] = False
            context['titulo'] = "Nuevo Pedido"
            return render(self.request, self.template_name, context)
        context = self.get_context_data()
        self.request.session['paquetes'] = paquetes
        context['paquetes'] = paquetes
        form.add_error(None, 'El formulario no es válido. Se encontraron errores.')
        context['titulo'] = "Nuevo Pedido"
        if form.errors:
            errores=[]
            if not form.errors.get('peso') == None:
                errores.append(form.errors.get('peso')[0])
            if not form.errors.get('ancho') == None:
                 errores.append(form.errors.get('ancho')[0])
            if not form.errors.get('largo') == None:
                 errores.append(form.errors.get('largo')[0])
            if not form.errors.get('alto') == None:
                 errores.append(form.errors.get('alto')[0]) 
            context['errores'] = errores              
            # return self.render_to_response(self.get_context_data(form=form))
            # return render(self.request, self.template_name, {'form': form, 'messages': messages})
        return render(self.request, self.template_name, context)
    def get_context_data(self, **kwargs):
        
        self.request.session['paquetes'] = []
        context = super().get_context_data(**kwargs)
        context['pedido_form'] = PedidoForm() 
        context['inicio'] = True
        context['titulo'] = "Nuevo Paquete"
        context['form'] = PaqueteForm()
        context['headers'] = [ 'Paquete', 'Peso', 'Ancho', 'Largo', 'Alto', 'Accion']

        return context

    
class ClienteCreateView(CreateView):
    '''Devuelve el formulario de registro del nuevo cliente'''
    template_name = 'core/pages/registrar_cliente.html'
    form_class = ClienteForm

    def post(self, request, *args, **kwargs):
        cliente = self.form_class(request.POST)
        if cliente.is_valid():
            cliente.save()
        return redirect('login')

class PedidoCreateView(LoginRequiredMixin, CreateView):
    '''Devuelve el formulario de solicitud de envío'''
    template_name = 'core/pages/registrar_pedido.html'
    form_class = PedidoForm
    success_url = '/clientes/'

    def form_valid(self, form):
        return super().form_valid(form)

class EmpleadosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''Recibe los datos del usuario y devuelve la vista de empleados.'''
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Pedido
    template_name = 'core/pages/empleados.html'
    ordering = ['id']

    def test_func(self):
        return self.request.user.groups.filter(name='empleado').exists()
        
    def get_queryset(self):
        postulante = Postulante.objects.get(user_ptr_id=self.request.user.id)
        empleado = Empleado.objects.filter(postulante=postulante).first()
        queryset = Pedido.objects.filter(asignacionpedido__empleado=empleado).all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Pedidos"
        context['headers'] = [ 'Id Pedido', 'Fecha pedido', 'Lugar de Entrega', 'Localidad/Provincia' ]
        context['fecha'] = self.kwargs['fecha']
        return context

def exit(request):
    '''Cierre la sesión y envía al home'''
    logout(request)
    return redirect('home')

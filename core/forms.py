from django import forms
from django.forms import ValidationError, ModelForm, modelformset_factory
from django.core.validators import validate_email
from .models import Domicilio, Pedido, Paquete
from django.contrib.auth.models import User

def sin_espacios(value):
    '''Remueve espacios al str que recibe "value"
    para que funcionen isdigit y isalpha'''
    return str(value).replace(' ','')

def solo_caracteres(value):
    """Si el valor ingresado tiene números, falla"""
    if sin_espacios(value).isdigit():
        raise ValidationError('El valor no puede contener números. %(valor)s',
                              params={'valor': value})

def solo_numeros(value):
    """Si el valor ingresado no cumple con el formato indicado, falla"""
    if sin_espacios(value).isalpha():
        raise ValidationError('El valor no puede contener letras. %(valor)s',
                              params={'valor': value})

def validar_mail(value):
    """Usa default validator de django para verificar el formato del mail"""
    try:
        validate_email(value)
    except ValidationError as exc:
        raise ValidationError('Ingrese una dirección de e-mail válida.') from exc

class ContactoForm(forms.Form):
    """Devuelve el formulario de contactos"""
    nombre = forms.CharField(
        label='Nombre',
        max_length=50,
        required=True,
        validators=[solo_caracteres],
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Solo letras'})
    )
    apellido = forms.CharField(
        label='Apellido',
        max_length=50,
        required=True,
        validators=[solo_caracteres],
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Solo letras'})
    )
    dni = forms.CharField(
         label="DNI",
         max_length=8,
         required=True,
         validators=[solo_numeros],
         widget=forms.TextInput(attrs={'class': 'form-control',
                                       'type':'number',
                                       'placeholder': 'Solo números'})
    )
    mail = forms.EmailField(
        label='Email',
        max_length=100,
        required=True,
        validators=[validar_mail],
        error_messages={'required': 'Por favor, completa el campo'},
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'type': 'email',
                                       'placeholder':'Introduzca dirección de email'})
    )
    curriculum = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(
        label='Mensaje',
        max_length=500,
        widget=forms.Textarea(attrs={'rows': '7',
                                     'class': 'form-control'})
    )

DomicilioFormSet = modelformset_factory(Domicilio, fields='__all__', extra=1)

PaqueteFormSet = modelformset_factory(Paquete, fields='__all__', widgets={'pedido': forms.HiddenInput()}, extra=1)

class PedidoForm(ModelForm):
    """Crea el formulario de pedidos"""
    class Meta:
        model = Pedido
        fields = '__all__'
        iddomicilio = DomicilioFormSet(queryset=Domicilio.objects.none(), prefix='domicilio')
        paquetes = PaqueteFormSet(queryset=Paquete.objects.none(), prefix='paquetes')
        widgets = {
            'iddomicilio': forms.HiddenInput(),
        }

class ClienteForm(ModelForm):
    fields = '__all__'
    iddomicilio = DomicilioFormSet(queryset=Domicilio.objects.none(), prefix='domicilio')
    password = forms.CharField(label='Contraseña',widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(label='Confirmar contraseña',widget=forms.PasswordInput, min_length=6)

    def clean_mail(self):
        if User.objects.filter(username=self.cleaned_data['mail']).exists():
            raise ValidationError("El cliente ya está registrado")
        return self.cleaned_data['mail']
    
    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            print("La contraseña no es correcta")
            raise ValidationError("La contraseña no coincide")
        return self.cleaned_data

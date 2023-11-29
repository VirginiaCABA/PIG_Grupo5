from django import forms
from django.forms import ValidationError, ModelForm
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Pedido, Cliente, Domicilio, Paquete, EstadoPedido

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
    first_name = forms.CharField(
        label='Nombre',
        max_length=50,
        required=True,
        validators=[solo_caracteres],
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Solo letras'})
    )
    last_name = forms.CharField(
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
    email = forms.EmailField(
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

class PedidoForm(ModelForm):
    estado = forms.CharField(label="estado", initial=EstadoPedido.RECIBIDO.label, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    # domicilio = forms.ModelChoiceField(label="domicilio", queryset=Domicilio.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    provincia = forms.CharField(label='Provincia', max_length=150, required=True,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo letras'}))
    localidad = forms.CharField(label='Localidad', max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo letras'}))
    calle = forms.CharField(label='Calle', max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo letras'}))
    numero = forms.CharField(label="Numero", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Solo números'}))
    piso = forms.CharField(label="Piso", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Solo números'}))
    departamento = forms.CharField(label='Departamento', max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo letras'}))
    cp = forms.CharField(label="cp", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Solo números'}))

    class Meta:
        model = Pedido
        fields=['provincia','localidad','calle','numero','piso','departamento','cp']   


class PaqueteForm(ModelForm):
    peso = forms.CharField(label="Peso", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo números'}))
    ancho = forms.CharField(label="Ancho", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo números'}))
    largo = forms.CharField(label="Largo", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo números'}))
    alto = forms.CharField(label="Alto", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo números'}))

    class Meta:
        model = Paquete
        fields = ['peso', 'ancho', 'largo', 'alto']

    def clean_peso(self):
        peso = self.cleaned_data.get('peso')

        if peso is not None:
            try:
                decimal_peso = float(peso)
                return decimal_peso
            except ValueError:
                raise forms.ValidationError('Ingrese un valor numérico válido en el campo Peso.')
        else:
            raise forms.ValidationError('Este campo es requerido.')
        
    def clean_ancho(self):
        ancho = self.cleaned_data.get('ancho')

        if ancho is not None:
            try:
                decimal_ancho = float(ancho)
                return decimal_ancho
            except ValueError:
                raise forms.ValidationError('Ingrese un valor numérico válido en el campo Ancho.')
        else:
            raise forms.ValidationError('Este campo es requerido.')
        
    def clean_largo(self):
        largo = self.cleaned_data.get('largo')

        if largo is not None:
            try:
                decimal_largo = float(largo)
                return decimal_largo
            except ValueError:
                raise forms.ValidationError('Ingrese un valor numérico válido en el campo Largo.')
        else:
            raise forms.ValidationError('Este campo es requerido.')
        

    def clean_alto(self):
        alto = self.cleaned_data.get('alto')

        if alto is not None:
            try:
                decimal_alto = float(alto)
                return decimal_alto
            except ValueError:
                raise forms.ValidationError('Ingrese un valor numérico válido en el campo Alto.')
        else:
            raise forms.ValidationError('Este campo es requerido.')


class DomicilioForm(ModelForm):

    class Meta:
        model = Domicilio
        fields = ['calle', 'numero', 'piso', 'departamento', 'localidad', 'cp']
        exclude = ['baja']
        
class ClienteForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El cliente ya está registrado")
        return email
    
    class Meta:
        model = Cliente
        fields = ['email', 'password', 'first_name', 'last_name', 'cuit', 'domicilio']

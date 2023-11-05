from django import forms
from django.forms import ValidationError
from django.core.validators import validate_email

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

class PedidoForm(forms.Form):
    """Devuelve el formulario de pedidos"""
    SERVICIOS_CHOICES = [
        ("", "Seleccionar..."),
        ("1", "Servicios en gral."),
        ("1", "Courier - Mensajería - Cadetes fijos"),
        ("2", "Transportes y cargas"),
        ("3", "E-Commerce y distribución de paquetería")
    ]

    servicios = forms.ChoiceField(label="Tipo de Servicio",
                                  widget=forms.Select, choices=SERVICIOS_CHOICES, required=True)

    direccion = forms.CharField(label="* Dirección", max_length="100", required=True,
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    codigo_postal = forms.CharField(label="* Código Postal", max_length="100", required=True,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))

    altura = forms.CharField(label="* Altura", max_length="100", required=True,
                             widget=forms.TextInput(attrs={"class": "form-control"}))

    piso_dpto = forms.CharField(label="Piso/Dpto (opcional)", max_length="100",
                                widget=forms.TextInput(attrs={"class": "form-control"}))

    instrucciones = forms.CharField(label="Instrucciones (opcional)", max_length="100",
                                    widget=forms.TextInput(attrs={"class": "form-control"}))

    nombre = forms.CharField(label="* Nombre", max_length="100", required=True,
                             widget=forms.TextInput(attrs={"class": "form-control"}))

    telefono = forms.DecimalField(label="* Telefono", max_digits="20", required=True,
                                  widget=forms.NumberInput(attrs={"class": "form-control"}))

    nombre_alternativo = forms.CharField(label="* Nombre Alternativo", max_length="100", required=True,
                                         widget=forms.TextInput(attrs={"class": "form-control"}))

    telefono_alternativo = forms.DecimalField(label="* Telefono Alternativo", max_digits="20", required=True,
                                              widget=forms.NumberInput(attrs={"class": "form-control"}))

    PAQUETE_CHOICES = [
		("", "Seleccionar..."),
		("1", "Sobre - Mensajero con mochila (Documentos, libros, sobres, etc)"),
		("2", "Caja pequeña - Máximo: Ancho:39.5 cm Alto:30.5cm, Peso: 1kg"),
		("3", "Caja mediana - Máximo: 30 L x 40 An x 30 Al (Hasta 15KG)"),
		("4", "Caja grande - Máximo: 40L x 50 An x 40 Al. (Hasta 25kg)")
	]

    paquete = forms.ChoiceField( label="Tipo de paquete",
                                widget=forms.Select, choices=PAQUETE_CHOICES, required=True)

    referencia = forms.CharField(label="Referencia", max_length="100",
                                 widget=forms.TextInput(attrs={"class": "form-control"}))

    comentarios = forms.CharField(label="Comentarios", max_length="100",
                                  widget=forms.Textarea(attrs={"class": "form-control"}))

import re
from django import forms
from django.forms import ValidationError

class CreateCostumerForm(forms.Form):
	SERVICIOS_CHOICES = [
		("", "Servicios"),
		("1", "Courier - Mensajería - Cadetes fijos"),
		("2", "Transportes y cargas"),
		("3", "E-Commerce y distribución de paquetería")
	]
	servicios = forms.ChoiceField(label="Elige el servicio a contratar", widget=forms.Select, choices=SERVICIOS_CHOICES, required=True,
	)
	dom1 = forms.CharField(label="Dirección recolección", max_length="100", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
	cp1 = forms.CharField(label="Código Postal", max_length="100", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
	nroExt1 = forms.CharField(label="No. Exterior (altura)", max_length="100", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
	nroInt1 = forms.CharField(label="No. Interior (opcional)", max_length="100", widget=forms.TextInput(attrs={"class": "form-control"}))
	instruc = forms.CharField(label="Instrucciones (opcional)", max_length="100", widget=forms.TextInput(attrs={"class": "form-control"}))

	nombre1 = forms.CharField(label="Nombre *", max_length="100", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
	telefono1 = forms.DecimalField(label="Telefono *", max_digits="20", required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
 
	nombre2 = forms.CharField(label="Nombre *", max_length="100", required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
	telefono2 = forms.DecimalField(label="Telefono *", max_digits="20", required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))

	PAQUETE_CHOICES = [
		("", "Elige el tipo de paquete"),
		("1", "Sobre - Mensajero con mochila (Documentos, libros, sobres, etc)"),
		("2", "Caja pequeña - Máximo: Ancho:39.5 cm Alto:30.5cm, Peso: 1kg"),
		("3", "Caja mediana - Máximo: 30 L x 40 An x 30 Al (Hasta 15KG)"),
		("4", "Caja grande - Máximo: 40L x 50 An x 40 Al. (Hasta 25kg)")
	]
	paquete = forms.ChoiceField( label="Elige el tipo de paquete", widget=forms.Select, choices=PAQUETE_CHOICES, required=True)

	referencia = forms.CharField(label="Referencia", max_length="100", widget=forms.TextInput(attrs={"class": "form-control"}))
	comentarios = forms.CharField(label="Comentarios", max_length="100", widget=forms.Textarea(attrs={"class": "form-control"}))

def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre no puede contener números. %(valor)s', code='Invalid', params={'valor': value})

#no esta lista   
def solo_numeros(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El DNI no puede contener letras. %(valor)s', code='Invalid', params={'valor': value}) 
#corregir funcion solo_numeros

def custom_validate_email(value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError('Correo electrónico inválido')

class ContactoForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre de contacto',
        max_length=50,
        required=True, 
        validators=(solo_caracteres,),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo letras'})
    )
    apellido = forms.CharField(
        label='Apellido de contacto',
        max_length=50,
        required=True, 
        validators=(solo_caracteres,),
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Solo letras'})
    )
    dni = forms.CharField(
         label="DNI de contacto" , 
         max_length=8,
         required=True, 
         validators=(solo_numeros,),
         widget=forms.TextInput(attrs={'class': 'form-control','type':'number','placeholder': 'Solo números'})
    )    
    mail = forms.EmailField(
        label='Email',
        max_length=100,
        required=True,
        validators=(custom_validate_email,),
        error_messages={'required': 'Por favor completa el campo'},
        widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email','placeholder':'Introduzca email'})
    )
    mensaje = forms.CharField(
        label='Mensaje',
        max_length=500,
        widget=forms.Textarea(attrs={'rows': 10, 'class': 'form-control'})
    )
    curriculun = forms.FileField(label="Curriculum" ,required=True)
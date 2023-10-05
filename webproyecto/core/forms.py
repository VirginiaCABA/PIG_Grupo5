from django import forms

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

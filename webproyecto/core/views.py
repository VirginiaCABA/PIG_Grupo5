from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request ,"core/home.html")

def nosotros(request):
    return render(request ,"core/nosotros.html")

def servicios(request):
     return render(request ,"core/servicios.html")

def contacto(request):
     return render(request ,"core/contacto.html")



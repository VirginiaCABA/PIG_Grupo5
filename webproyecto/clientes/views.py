from django.shortcuts import render
from .models import Project

# Create your views here.
def clientes(request):
     projects = Project.objects.all()
     return render(request ,"clientes/clientes.html", {'projects': projects})
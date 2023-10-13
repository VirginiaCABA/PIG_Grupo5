from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
#create table
class Contacto(models.Model):
    id = models.AutoField(primary_key=True),
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True) 
    dni =  models.CharField(max_length=10, validators=[RegexValidator(r'^\d{8,10}$', message='El número de dni debe tener entre 8 y 10 dígitos.')])
    mail = models.EmailField(max_length=100, unique=True)
    curriculum = models.FileField(upload_to='cv_upload/')
    mensaje = models.TextField(max_length=500, blank=True, null=True)
    class Meta:
            app_label = 'core'
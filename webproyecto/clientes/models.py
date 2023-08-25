from django.db import models

# Create your models here.
class Project(models.Model):
    client = models.CharField(max_length=200, verbose_name='Cliente')
    description = models.TextField(verbose_name='Descripción')
    image = models.ImageField(verbose_name='Imagen',upload_to='projects') #or_clients
    link = models.URLField(verbose_name= "Pagina web", null = True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')

    def __str__(self):
        return self.client    

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        ordering = ['-created']



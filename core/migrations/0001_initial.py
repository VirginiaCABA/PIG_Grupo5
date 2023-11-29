# Generated by Django 4.1 on 2023-11-29 20:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsignacionPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('baja', models.BooleanField(default=False)),
                ('cuit', models.BigIntegerField(verbose_name='CUIT')),
            ],
            options={
                'verbose_name_plural': 'Clientes',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Domicilio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(max_length=150, verbose_name='Calle')),
                ('numero', models.IntegerField(verbose_name='Número')),
                ('piso', models.IntegerField(verbose_name='Piso')),
                ('departamento', models.CharField(max_length=150, verbose_name='Dpto')),
                ('cp', models.IntegerField(verbose_name='Código Postal')),
                ('latitud', models.FloatField(null=True, verbose_name='Latitud')),
                ('longitud', models.FloatField(null=True, verbose_name='Longitud')),
                ('baja', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Domicilios',
            },
        ),
        migrations.CreateModel(
            name='Postulante',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('baja', models.BooleanField(default=False)),
                ('dni', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{8,10}$', message='El número de dni debe tener entre 8 y 10 dígitos.')], verbose_name='DNI')),
                ('curriculum', models.FileField(upload_to='cv_upload/')),
                ('mensaje', models.TextField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name_plural': 'Postulantes',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('baja', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('numero', models.IntegerField(verbose_name='Número')),
                ('baja', models.BooleanField(default=False)),
                ('domicilio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.domicilio')),
            ],
            options={
                'verbose_name_plural': 'Sucursales',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('idpedido', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('1', 'Recibido'), ('2', 'Procesado'), ('3', 'Asignado'), ('4', 'Entregado'), ('5', 'No entregado en 1er visita'), ('6', 'No entregado en 2da visita')], default='1', max_length=3)),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
                ('domicilio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.domicilio')),
            ],
        ),
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField(verbose_name='Peso')),
                ('ancho', models.FloatField(verbose_name='Ancho')),
                ('largo', models.FloatField(verbose_name='Largo')),
                ('alto', models.FloatField(verbose_name='Alto')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('baja', models.BooleanField(default=False)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.provincia')),
            ],
            options={
                'verbose_name_plural': 'Localidades',
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baja', models.BooleanField(default=False)),
                ('pedidos', models.ManyToManyField(through='core.AsignacionPedido', to='core.pedido')),
                ('postulante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.postulante')),
            ],
            options={
                'verbose_name_plural': 'Empleados',
            },
        ),
        migrations.AddField(
            model_name='domicilio',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.localidad'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='domicilio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.domicilio'),
        ),
        migrations.AddField(
            model_name='asignacionpedido',
            name='empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.empleado'),
        ),
        migrations.AddField(
            model_name='asignacionpedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pedido'),
        ),
    ]

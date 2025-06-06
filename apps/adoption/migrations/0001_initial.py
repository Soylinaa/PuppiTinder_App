# Generated by Django 5.1.7 on 2025-05-26 17:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.CharField(max_length=50)),
                ('breed', models.CharField(max_length=100)),
                ('size', models.CharField(choices=[('pequeño', 'Pequeño'), ('mediano', 'Mediano'), ('grande', 'Grande')], max_length=20)),
                ('gender', models.CharField(choices=[('macho', 'Macho'), ('hembra', 'Hembra')], max_length=10)),
                ('personality', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='dogs/')),
                ('status', models.CharField(choices=[('disponible', 'Disponible'), ('en_proceso', 'En proceso de adopción'), ('adoptado', 'Adoptado'), ('no_disponible', 'No disponible')], default='disponible', max_length=20)),
                ('is_vaccinated', models.BooleanField(default=False)),
                ('is_sterilized', models.BooleanField(default=False)),
                ('special_needs', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Perro',
                'verbose_name_plural': 'Perros',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AdoptionApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('housing_type', models.CharField(choices=[('casa', 'Casa con jardín'), ('apartamento', 'Apartamento'), ('casa_sin_jardin', 'Casa sin jardín')], max_length=20)),
                ('experience', models.CharField(choices=[('primera_vez', 'Primera vez'), ('poca', 'Poca experiencia'), ('moderada', 'Experiencia moderada'), ('mucha', 'Mucha experiencia')], max_length=20)),
                ('size_preference', models.CharField(choices=[('pequeño', 'Pequeño'), ('mediano', 'Mediano'), ('grande', 'Grande'), ('cualquiera', 'Cualquiera')], max_length=20)),
                ('motivation', models.TextField()),
                ('available_time', models.CharField(choices=[('1-2-horas', '1-2 horas'), ('3-4-horas', '3-4 horas'), ('5-6-horas', '5-6 horas'), ('todo-el-dia', 'Todo el día')], max_length=20)),
                ('accepts_terms', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_revision', 'En revisión'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('completada', 'Completada')], default='pendiente', max_length=20)),
                ('admin_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applicant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adoption_applications', to=settings.AUTH_USER_MODEL)),
                ('matched_dog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applications', to='adoption.dog')),
            ],
            options={
                'verbose_name': 'Solicitud de Adopción',
                'verbose_name_plural': 'Solicitudes de Adopción',
                'ordering': ['-created_at'],
            },
        ),
    ]

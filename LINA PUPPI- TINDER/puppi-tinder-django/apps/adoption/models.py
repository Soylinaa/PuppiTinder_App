from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Dog(models.Model):
    SIZE_CHOICES = [
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
    ]
    
    GENDER_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_proceso', 'En proceso de adopción'),
        ('adoptado', 'Adoptado'),
        ('no_disponible', 'No disponible'),
    ]

    name = models.CharField(max_length=100)
    age = models.CharField(max_length=50)  # "2 años", "6 meses", etc.
    breed = models.CharField(max_length=100)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    personality = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='dogs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponible')
    is_vaccinated = models.BooleanField(default=False)
    is_sterilized = models.BooleanField(default=False)
    special_needs = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perro'
        verbose_name_plural = 'Perros'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.breed}"

class AdoptionApplication(models.Model):
    HOUSING_CHOICES = [
        ('casa', 'Casa con jardín'),
        ('apartamento', 'Apartamento'),
        ('casa_sin_jardin', 'Casa sin jardín'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('primera_vez', 'Primera vez'),
        ('poca', 'Poca experiencia'),
        ('moderada', 'Experiencia moderada'),
        ('mucha', 'Mucha experiencia'),
    ]
    
    SIZE_PREFERENCE_CHOICES = [
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
        ('cualquiera', 'Cualquiera'),
    ]
    
    TIME_CHOICES = [
        ('1-2-horas', '1-2 horas'),
        ('3-4-horas', '3-4 horas'),
        ('5-6-horas', '5-6 horas'),
        ('todo-el-dia', 'Todo el día'),
    ]
    
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En revisión'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('completada', 'Completada'),
    ]

    # Información personal
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_applications', null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    # Preferencias de adopción
    housing_type = models.CharField(max_length=20, choices=HOUSING_CHOICES)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    size_preference = models.CharField(max_length=20, choices=SIZE_PREFERENCE_CHOICES)
    
    # Compromiso
    motivation = models.TextField()
    available_time = models.CharField(max_length=20, choices=TIME_CHOICES)
    accepts_terms = models.BooleanField(default=False)
    
    # Resultado del matching
    matched_dog = models.ForeignKey(Dog, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    
    # Estado de la aplicación
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Solicitud de Adopción'
        verbose_name_plural = 'Solicitudes de Adopción'
        ordering = ['-created_at']

    def __str__(self):
        return f"Solicitud de {self.full_name} - {self.status}"
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_adopter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    housing_type = models.CharField(max_length=50, choices=[
        ('casa', 'Casa con jardín'),
        ('apartamento', 'Apartamento'),
        ('casa_sin_jardin', 'Casa sin jardín'),
    ], blank=True)
    experience_with_dogs = models.CharField(max_length=50, choices=[
        ('primera_vez', 'Primera vez'),
        ('poca', 'Poca experiencia'),
        ('moderada', 'Experiencia moderada'),
        ('mucha', 'Mucha experiencia'),
    ], blank=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
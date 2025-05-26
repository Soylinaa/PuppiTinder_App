from django.contrib import admin
from .models import Dog, AdoptionApplication

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'size', 'gender', 'status', 'created_at')
    list_filter = ('status', 'size', 'gender', 'is_vaccinated', 'is_sterilized')
    search_fields = ('name', 'breed', 'personality')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'status', 'matched_dog', 'created_at')
    list_filter = ('status', 'housing_type', 'experience', 'size_preference')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
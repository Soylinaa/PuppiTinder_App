from rest_framework import serializers
from .models import Dog, AdoptionApplication

class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = '__all__'

class AdoptionApplicationSerializer(serializers.ModelSerializer):
    matched_dog_data = DogSerializer(source='matched_dog', read_only=True)
    
    class Meta:
        model = AdoptionApplication
        fields = '__all__'
        read_only_fields = ('applicant', 'matched_dog', 'status', 'admin_notes', 'created_at', 'updated_at')
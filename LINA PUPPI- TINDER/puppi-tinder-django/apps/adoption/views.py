import random
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Dog, AdoptionApplication
from .serializers import DogSerializer, AdoptionApplicationSerializer

class DogListView(generics.ListAPIView):
    queryset = Dog.objects.filter(status='disponible')
    serializer_class = DogSerializer
    permission_classes = [AllowAny]

class DogDetailView(generics.RetrieveAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir solicitudes sin autenticación
def submit_adoption_application(request):
    serializer = AdoptionApplicationSerializer(data=request.data)
    
    if serializer.is_valid():
        # Si hay usuario autenticado, lo asignamos, sino creamos la solicitud sin usuario
        if request.user.is_authenticated:
            application = serializer.save(applicant=request.user)
        else:
            application = serializer.save()
        
        # Algoritmo de matching simple
        matched_dog = find_matching_dog(application)
        if matched_dog:
            application.matched_dog = matched_dog
            application.save()
        
        return Response(AdoptionApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications(request):
    applications = AdoptionApplication.objects.filter(applicant=request.user)
    serializer = AdoptionApplicationSerializer(applications, many=True)
    return Response(serializer.data)

def find_matching_dog(application):
    """Algoritmo simple de matching basado en preferencias"""
    available_dogs = Dog.objects.filter(status='disponible')
    
    # Filtrar por tamaño preferido
    if application.size_preference != 'cualquiera':
        preferred_dogs = available_dogs.filter(size=application.size_preference)
        if preferred_dogs.exists():
            available_dogs = preferred_dogs
    
    # Filtrar por experiencia (perros más fáciles p
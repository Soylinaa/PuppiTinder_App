from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductListSerializer, ProductCategorySerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        
        # Filtros
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        brand = self.request.query_params.get('brand', None)
        free_shipping = self.request.query_params.get('free_shipping', None)
        
        if category:
            queryset = queryset.filter(category__slug=category)
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(brand__icontains=search) | 
                Q(description__icontains=search)
            )
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        if brand:
            queryset = queryset.filter(brand__icontains=brand)
        
        if free_shipping:
            queryset = queryset.filter(free_shipping=True)
        
        # Ordenamiento
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering in ['price', '-price', 'rating', '-rating', 'name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(ordering)
        
        return queryset

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductCategoryListView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_products(request):
    """Productos destacados (con mejor rating o más recientes)"""
    products = Product.objects.filter(is_available=True).order_by('-rating', '-created_at')[:8]
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_brands(request):
    """Lista de marcas disponibles"""
    brands = Product.objects.filter(is_available=True).values_list('brand', flat=True).distinct().order_by('brand')
    return Response(list(brands))
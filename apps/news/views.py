from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import News, NewsCategory, NewsComment
from .serializers import NewsSerializer, NewsListSerializer, NewsCategorySerializer, NewsCommentSerializer

class NewsListView(generics.ListAPIView):
    serializer_class = NewsListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        featured = self.request.query_params.get('featured', None)
        
        if category:
            queryset = queryset.filter(category__slug=category)
        if search:
            queryset = queryset.filter(title__icontains=search)
        if featured:
            queryset = queryset.filter(is_featured=True)
            
        return queryset.order_by('-published_at')

class NewsDetailView(generics.RetrieveAPIView):
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return News.objects.filter(is_published=True)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class NewsCategoryListView(generics.ListAPIView):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, slug):
    news = get_object_or_404(News, slug=slug, is_published=True)
    serializer = NewsCommentSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(author=request.user, news=news)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_news(request):
    news = News.objects.filter(is_published=True, is_featured=True)[:5]
    serializer = NewsListSerializer(news, many=True)
    return Response(serializer.data)
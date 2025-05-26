from rest_framework import serializers
from .models import News, NewsCategory, NewsComment

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = '__all__'

class NewsCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = NewsComment
        fields = ('id', 'content', 'author_name', 'created_at', 'is_approved')
        read_only_fields = ('id', 'created_at', 'is_approved')

class NewsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    comments = NewsCommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = (
            'id', 'title', 'slug', 'summary', 'content', 'category', 'category_name', 
            'category_color', 'author', 'author_name', 'image', 'is_published', 
            'is_featured', 'views_count', 'created_at', 'updated_at', 'published_at',
            'comments', 'comments_count'
        )
        read_only_fields = ('id', 'views_count', 'created_at', 'updated_at')

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

class NewsListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = (
            'id', 'title', 'slug', 'summary', 'category_name', 'category_color',
            'author_name', 'image', 'is_featured', 'views_count', 'created_at',
            'published_at', 'comments_count'
        )

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
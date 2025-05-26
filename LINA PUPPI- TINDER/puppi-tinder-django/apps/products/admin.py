from django.contrib import admin
from .models import Product, ProductCategory

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'source_site', 'is_available', 'last_scraped')
    list_filter = ('category', 'brand', 'source_site', 'is_available', 'free_shipping')
    search_fields = ('name', 'brand', 'description')
    readonly_fields = ('last_scraped', 'created_at', 'updated_at', 'discount_percentage')
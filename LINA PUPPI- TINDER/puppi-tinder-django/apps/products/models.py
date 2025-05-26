from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoría de Producto'
        verbose_name_plural = 'Categorías de Productos'

    def __str__(self):
        return self.name

class Product(models.Model):
    # Información básica del producto
    name = models.CharField(max_length=200)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    
    # Precios
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Información del scraping
    source_url = models.URLField(blank=True)
    source_site = models.CharField(max_length=100, blank=True)
    external_id = models.CharField(max_length=100, blank=True)
    
    # Imágenes y media
    image_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Disponibilidad y stock
    is_available = models.BooleanField(default=True)
    stock_status = models.CharField(max_length=50, blank=True)
    
    # Rating y reviews
    rating = models.FloatField(default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    
    # Información adicional
    free_shipping = models.BooleanField(default=False)
    features = models.JSONField(default=list, blank=True)
    
    # Metadatos
    last_scraped = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.brand}"

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100)
        return 0
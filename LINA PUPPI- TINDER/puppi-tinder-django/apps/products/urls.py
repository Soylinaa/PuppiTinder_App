from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('categories/', views.ProductCategoryListView.as_view(), name='product-categories'),
    path('brands/', views.product_brands, name='product-brands'),
    path('featured/', views.featured_products, name='featured-products'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]
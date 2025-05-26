from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='pages/inicio.html'), name='home'),
    #path('api/auth/', include('apps.users.urls')),
    path('api/news/', include('apps.news.urls')),
    path('api/adoption/', include('apps.adoption.urls')),
    path('api/products/', include('apps.products.urls')),
    path('noticias/', TemplateView.as_view(template_name='pages/noticias.html'), name='noticias'),
    path('adopcion/', TemplateView.as_view(template_name='pages/adopcion.html'), name='adopcion'),
    path('tienda/', TemplateView.as_view(template_name='pages/tienda.html'), name='tienda'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path
from . import views

urlpatterns = [
    path('dogs/', views.DogListView.as_view(), name='dog-list'),
    path('dogs/<int:pk>/', views.DogDetailView.as_view(), name='dog-detail'),
    path('apply/', views.submit_adoption_application, name='submit-application'),
    path('my-applications/', views.my_applications, name='my-applications'),
]
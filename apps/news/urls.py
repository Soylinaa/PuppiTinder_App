from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news-list'),
    path('categories/', views.NewsCategoryListView.as_view(), name='news-categories'),
    path('featured/', views.featured_news, name='featured-news'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add-comment'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('about/', views.about, name='about'),
    
    # API endpoints
    path('api/random-articles/', views.random_articles_api, name='random_articles_api'),
    path('api/calendar-data/', views.calendar_data_api, name='calendar_data_api'),
    path('api/articles/', views.article_list_api, name='article_list_api'),
]
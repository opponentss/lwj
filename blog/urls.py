from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('about/', views.about, name='about'),
    path('photos/', views.photo_wall, name='photo_wall'),
    path('photos/upload/', views.photo_upload, name='photo_upload'),
    path('photos/delete/<int:photo_id>/', views.photo_delete, name='photo_delete'),
    
    # 登录注册
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # API endpoints
    path('api/random-articles/', views.random_articles_api, name='random_articles_api'),
    path('api/calendar-data/', views.calendar_data_api, name='calendar_data_api'),
    path('api/articles/', views.article_list_api, name='article_list_api'),
]
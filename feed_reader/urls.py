from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/toggle_read/', views.toggle_read_status, name='toggle_read'),
    path('signup/', views.signup, name='signup'),
]

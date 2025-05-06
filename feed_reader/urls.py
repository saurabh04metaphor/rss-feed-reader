from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feed_list'),  # /feeds/
    path('articles/', views.article_list, name='all_articles'),  # New global articles view
    path('articles/<int:id>/', views.article_list, name='article_list'),  # Feed-specific articles
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/toggle_read/', views.toggle_read_status, name='toggle_read'),
    path('feed/<int:feed_id>/unsubscribe/', views.unsubscribe_feed, name='unsubscribe_feed'),
]

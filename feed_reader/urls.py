from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feed_list'),  # /feeds/
    path('articles/<int:id>/', views.article_list, name='article_list'),  # /feeds/articles/1/
    path('article/<int:pk>/', views.article_detail, name='article_detail'),  # /feeds/article/1/
    path('article/<int:pk>/toggle_read/', views.toggle_read_status, name='toggle_read'),  # /feeds/article/1/toggle_read/
    path('feed/<int:feed_id>/unsubscribe/', views.unsubscribe_feed, name='unsubscribe_feed'),  # /feeds/feed/1/unsubscribe/
]

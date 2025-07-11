from django.urls import path
from .views import PostListAPIView, PostDetailAPIView, PostExportAPIView, PostImportAPIView, PostStatsAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/export/', PostExportAPIView.as_view(), name='export json file'),
    path('posts/import/', PostImportAPIView.as_view(), name='import json file'),
    path('posts/stats/', PostStatsAPIView.as_view(), name='post-stats'),
]

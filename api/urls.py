from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path('cache/', views.cache_test_view),
]
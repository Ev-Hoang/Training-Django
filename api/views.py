from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def getData(request):
    person = {'name': "kien", 'age':20}
    return Response(person)

def cache_test_view(request):
    value = cache.get('test_key')
    if not value:
        value = "Hello from Redis!"
        cache.set('test_key', value, timeout=60)  # 60s
    return JsonResponse({'value': value})
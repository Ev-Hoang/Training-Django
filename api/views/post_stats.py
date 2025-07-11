from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from ..models import Post


class PostStatsAPIView(APIView):
    def get(self, request):
        try:
            stats = Post.objects.values('author').annotate(count=Count('id')).order_by('-count')
            return Response(stats)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

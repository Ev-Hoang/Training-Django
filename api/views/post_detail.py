from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Post
from drf_yasg.utils import swagger_auto_schema
from ..serializers import PostSerializer
from django.shortcuts import get_object_or_404

# /api/posts/<id>/
class PostDetailAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PostSerializer)
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
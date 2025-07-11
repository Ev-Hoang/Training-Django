from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404

class PostAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by title",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Ammount of blogs",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'offset',
                openapi.IN_QUERY,
                description="Offsets",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get(self, request):
        # Search theo title
        search_query = request.GET.get('search')
        posts = Post.objects.all()
        if search_query:
            posts = posts.filter(title__icontains=search_query)

        # Pagination: limit & offset
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        total = posts.count()

        posts = posts[offset:offset + limit]
        serializer = PostSerializer(posts, many=True)

        return Response({
            "total": total,
            "limit": limit,
            "offset": offset,
            "results": serializer.data
        })

    @swagger_auto_schema(request_body=PostSerializer)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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

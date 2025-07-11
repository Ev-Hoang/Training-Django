from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Post
from drf_yasg.utils import swagger_auto_schema
from ..serializers import PostSerializer

# /api/posts/<id>/
class PostDetailAPIView(APIView):
    def get(self, request, pk):
        """
        Lấy chi tiết một bài viết theo primary key (pk).

        Params:
        - request: request object của Django REST Framework.
        - pk (int): id của bài viết cần lấy.

        Trả về:
        - 200 + dữ liệu bài viết nếu tìm thấy.
        - 404 nếu bài viết không tồn tại.
        - 500 nếu lỗi server xảy ra.
        """
        try:
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                return Response({"error": "Post không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=PostSerializer)
    def put(self, request, pk):
        """
        Cập nhật một bài viết theo primary key (pk).

        Params:
        - request: request object chứa dữ liệu cập nhật.
        - pk (int): id của bài viết cần cập nhật.

        Trả về:
        - 200 + dữ liệu bài viết sau khi cập nhật nếu thành công.
        - 400 nếu dữ liệu đầu vào không hợp lệ.
        - 404 nếu bài viết không tồn tại.
        - 500 nếu lỗi server xảy ra.
        """
        try:
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                return Response({"error": "Post Undefined"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"error": "Data Incorrect", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """
        Xóa bài viết theo primary key (pk).

        Params:
        - request: request object.
        - pk (int): id của bài viết cần xóa.

        Trả về:
        - 204 nếu xóa thành công.
        - 404 nếu bài viết không tồn tại.
        - 500 nếu lỗi server xảy ra.
        """
        try:
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                return Response({"error": "Post Undefined"}, status=status.HTTP_404_NOT_FOUND)

            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
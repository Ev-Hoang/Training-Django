from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Post
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ValidationError
from ..serializers import PostSerializer, PostQuerySerializer

import traceback

# /api/posts/
class PostListAPIView(APIView):

    @swagger_auto_schema(query_serializer=PostQuerySerializer)
    def get(self, request):
        """
        Lấy danh sách bài viết với khả năng tìm kiếm và phân trang.

        Query parameters:
        - search (str, optional): Từ khóa tìm kiếm trong tiêu đề bài viết.
        - limit (int, optional): Số lượng bài viết trả về mỗi trang, mặc định 10.
        - offset (int, optional): Vị trí bắt đầu lấy dữ liệu (để phân trang), mặc định 0.

        Trả về:
        - 200: JSON chứa tổng số bài viết phù hợp (total), limit, offset, và danh sách kết quả.
        - 400: Nếu giá trị limit hoặc offset không hợp lệ.
        - 500: Lỗi server không mong muốn.
        """
        try:
            # Lấy dữ liệu query params
            search_query = request.GET.get('search')
            limit = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))

            # Lọc dữ liệu
            posts = Post.objects.all()
            if search_query:
                posts = posts.filter(title__icontains=search_query)

            total = posts.count()
            posts = posts[offset:offset + limit]
            serializer = PostSerializer(posts, many=True)

            return Response({
                "total": total,
                "limit": limit,
                "offset": offset,
                "results": serializer.data
            })

        except ValueError as e:
            return Response({"error": "Value Incorrect "}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=PostSerializer)
    def post(self, request):
        """
        Tạo mới một bài viết.

        Request body:
        - JSON chứa dữ liệu bài viết theo cấu trúc của PostSerializer.

        Trả về:
        - 201: Dữ liệu bài viết đã được tạo thành công.
        - 400: Dữ liệu gửi lên không hợp lệ (validation error).
        - 500: Lỗi server không mong muốn.
        """
        try:
            serializer = PostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response(
                {"error": "Validation failed", "details": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({"error": "Unexpected error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Post
from ..serializers import PostSerializer, PostFileUploadSerializer
from drf_yasg.utils import swagger_auto_schema
import json
import os
from django.conf import settings

JSON_FILE_PATH = os.path.join(settings.BASE_DIR, 'posts_data.json')

class PostExportAPIView(APIView):
    def get(self, request):
        try:
            posts = Post.objects.all()
            serializer = PostSerializer(posts, many=True)
            with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(serializer.data, f, ensure_ascii=False, indent=4)
            return Response({"message": f"Exported {len(serializer.data)} posts to {JSON_FILE_PATH}"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostImportAPIView(APIView):
    @swagger_auto_schema(request_body=PostFileUploadSerializer)
    def post(self, request):
        """
        Import danh sách bài viết từ file JSON trên server.

        Quy trình:
        - Kiểm tra sự tồn tại của file JSON theo đường dẫn JSON_FILE_PATH.
        - Đọc dữ liệu JSON từ file.
        - Dùng serializer để validate và lưu nhiều bài viết cùng lúc.

        Params:
        - request: request object (dùng để upload file hoặc trigger import).

        Trả về:
        - 200 với thông báo số bài viết đã import thành công.
        - 400 nếu file JSON không tồn tại hoặc dữ liệu không hợp lệ.
        - 500 nếu xảy ra lỗi hệ thống trong quá trình đọc hoặc lưu dữ liệu.
        """
        try:
            if not os.path.exists(JSON_FILE_PATH):
                return Response({"error": "JSON file not found"}, status=status.HTTP_400_BAD_REQUEST)

            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)

            serializer = PostSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": f"Imported {len(data)} posts from JSON file"})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

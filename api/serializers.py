from rest_framework import serializers
from .models import Post


class PostFileUploadSerializer(serializers.Serializer):
    """
    Serializer dùng để nhận file upload (ví dụ file JSON để import bài viết).
    
    Fields:
    - file: file upload, bắt buộc.
    """
    file = serializers.FileField()

class PostQuerySerializer(serializers.Serializer):
    """
    Serializer cho query params khi lấy danh sách bài viết.

    Fields:
    - search (str, optional): Từ khóa tìm kiếm trong tiêu đề.
    - limit (int, optional): Số lượng bài viết trả về (mặc định 10).
    - offset (int, optional): Vị trí bắt đầu lấy dữ liệu (mặc định 0).
    """
    search = serializers.CharField(required=False)
    limit = serializers.IntegerField(required=False, default=10)
    offset = serializers.IntegerField(required=False, default=0)

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer cho model Post, dùng cho CRUD.

    Fields:
    - title (str): Tiêu đề bài viết, bắt buộc, không được rỗng, tối đa 200 ký tự.
    - content (str): Nội dung bài viết, tối thiểu 10 ký tự.
    - author (str): Tên tác giả, bắt buộc, không được rỗng.
    - created_at (datetime, read-only): Thời gian tạo bài viết, định dạng ISO8601.
    """
    title = serializers.CharField(required=True, allow_blank=False)
    content = serializers.CharField(required=True, allow_blank=False)
    author = serializers.CharField(required=True, allow_blank=False)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("You must have a title.")
        if len(value) > 200:
            raise serializers.ValidationError("Title must be shorter than 200 characters.")
        return value

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("content must exceeded 10 characters.")
        return value

    def validate_author(self, value):
        if not value:
            raise serializers.ValidationError("You must have an author.")
        return value
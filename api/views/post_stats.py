from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from ..models import Post


class PostStatsAPIView(APIView):
    def get(self, request):
        """
        Lấy thống kê số lượng bài viết theo từng tác giả.

        Trả về:
        - 200: Danh sách các tác giả kèm số lượng bài viết của họ, sắp xếp giảm dần theo số lượng.
          Format mỗi phần tử: {"author": author_id, "count": số lượng bài viết}
        - 500: Nếu có lỗi server xảy ra.
        """
        try:
            stats = Post.objects.values('author').annotate(count=Count('id')).order_by('-count')
            return Response(stats)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

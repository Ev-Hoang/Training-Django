from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Dữ liệu giả lập (giống database)
posts = [
    {
        "id": 1,
        "title": "Bài viết đầu tiên",
        "content": "Nội dung bài viết...",
        "author": "Admin",
        "created_at": "2025-01-01T10:00:00"
    }
]


# /api/posts/
class PostListAPIView(APIView):
    def get(self, request):
        return Response(posts)

    def post(self, request):
        new_post = request.data
        new_post["id"] = posts[-1]["id"] + 1 if posts else 1
        posts.append(new_post)
        return Response(new_post, status=status.HTTP_201_CREATED)


# /api/posts/<id>/
class PostDetailAPIView(APIView):
    def get_object(self, pk):
        return next((p for p in posts if p["id"] == pk), None)

    def get(self, request, pk):
        post = self.get_object(pk)
        if post:
            return Response(post)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        post.update(request.data)
        return Response(post)

    def delete(self, request, pk):
        global posts
        posts = [p for p in posts if p["id"] != pk]
        return Response(status=status.HTTP_204_NO_CONTENT)
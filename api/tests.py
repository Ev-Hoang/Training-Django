from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Post

import traceback

class PostAPITests(APITestCase):
    def setUp(self):
        self.post1 = Post.objects.create(title="Test Post 1", content="Content 1", author="Author A")
        self.post2 = Post.objects.create(title="Another Post", content="Content 2", author="Author B")
        self.list_url = reverse('post-list')  # ex: path('posts/', PostListAPIView.as_view(), name='post-list')
        self.detail_url = lambda pk: reverse('post-detail', kwargs={'pk': pk})

    def test_list_posts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_list_posts_search(self):
        response = self.client.get(self.list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post 1')

    def test_list_posts_pagination(self):
        response = self.client.get(self.list_url, {'limit': 1, 'offset': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_post_valid(self):
        data = {
            "title": "Test Title",
            "content": "Test Content",
            "author": "Ev" 
        }
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_detail(self):
        response = self.client.get(self.detail_url(self.post1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post1.title)

    def test_get_post_detail_not_found(self):
        response = self.client.get(self.detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post(self):
        data = {"title": "Updated Title"}
        response = self.client.put(self.detail_url(self.post1.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, "Updated Title")

    def test_delete_post(self):
        response = self.client.delete(self.detail_url(self.post1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post1.pk).exists())
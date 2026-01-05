from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.posts.models import Post

User = get_user_model()


class PostViewSetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_list(self):
        Post.objects.create(
            user=self.user,
            content_type=Post.ContentType.TEXT,
            caption='Test post'
        )
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)


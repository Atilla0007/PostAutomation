from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.posts.models import Post, PostTarget
from apps.integrations.models import SocialAccount, Platform

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_post_creation(self):
        post = Post.objects.create(
            user=self.user,
            content_type=Post.ContentType.TEXT,
            caption='Test post'
        )
        self.assertEqual(str(post), f'{self.user.id}:TEXT:{post.id}')


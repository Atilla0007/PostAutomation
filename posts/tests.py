from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from posts.models import Post, PostTarget
from social.models import Platform, SocialAccount


class CapabilityEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='tester', password='pass1234')
        self.client.force_authenticate(self.user)

    def test_capabilities_endpoint(self):
        SocialAccount.objects.create(
            user=self.user,
            platform=Platform.YOUTUBE,
            display_name='YT',
        )
        response = self.client.get('/capabilities', {'content_type': 'VIDEO'})
        self.assertEqual(response.status_code, 200)
        platforms = {item['platform']: item for item in response.json()}
        self.assertTrue(platforms['youtube']['available'])


class PublishValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='tester', password='pass1234')
        self.client.force_authenticate(self.user)

    def test_publish_rejects_ineligible_targets(self):
        account_ok = SocialAccount.objects.create(
            user=self.user,
            platform=Platform.INSTAGRAM,
            display_name='IG Pro',
            account_type=SocialAccount.AccountType.INSTAGRAM_PROFESSIONAL,
            permissions_valid=True,
        )
        account_bad = SocialAccount.objects.create(
            user=self.user,
            platform=Platform.X,
            display_name='X',
            x_media_upload_enabled=False,
        )
        post = Post.objects.create(
            user=self.user,
            content_type=Post.ContentType.PHOTO,
            caption='Test',
            hashtags=['#tag'],
            image_file=SimpleUploadedFile('photo.jpg', b'filecontent'),
        )
        PostTarget.objects.create(post=post, social_account=account_ok)
        PostTarget.objects.create(post=post, social_account=account_bad)

        response = self.client.post(f'/posts/{post.id}/publish')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload['queued_post_target_ids']), 1)
        self.assertEqual(len(payload['rejected']), 1)

        account_ok_target = PostTarget.objects.get(post=post, social_account=account_ok)
        account_bad_target = PostTarget.objects.get(post=post, social_account=account_bad)
        self.assertEqual(account_ok_target.status, PostTarget.Status.QUEUED)
        self.assertEqual(account_bad_target.status, PostTarget.Status.REJECTED)

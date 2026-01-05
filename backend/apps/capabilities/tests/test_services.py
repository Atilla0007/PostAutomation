from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.capabilities.services.availability_service import (
    REASON_IG_PERMS_MISSING,
    REASON_IG_PRO_REQUIRED,
    REASON_TIKTOK_PREREQS,
    REASON_X_MEDIA_DISABLED,
    REASON_YT_VIDEO_ONLY,
    evaluate_availability,
)
from apps.integrations.models import Platform, SocialAccount


class CapabilityServiceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='tester', password='pass1234')

    def _get_platform(self, availability, platform):
        return next(item for item in availability if item.platform == platform)

    def test_youtube_video_only(self):
        SocialAccount.objects.create(
            user=self.user,
            platform=Platform.YOUTUBE,
            display_name='YT',
        )

        availability_text = evaluate_availability(self.user, 'TEXT', None)
        youtube_text = self._get_platform(availability_text, Platform.YOUTUBE.value)
        self.assertFalse(youtube_text.available)
        self.assertEqual(youtube_text.reason, REASON_YT_VIDEO_ONLY)

        availability_video = evaluate_availability(self.user, 'VIDEO', None)
        youtube_video = self._get_platform(availability_video, Platform.YOUTUBE.value)
        self.assertTrue(youtube_video.available)

    def test_instagram_requires_professional(self):
        SocialAccount.objects.create(
            user=self.user,
            platform=Platform.INSTAGRAM,
            display_name='IG',
            account_type=SocialAccount.AccountType.INSTAGRAM_PERSONAL,
            permissions_valid=True,
        )
        availability = evaluate_availability(self.user, 'TEXT', None)
        instagram = self._get_platform(availability, Platform.INSTAGRAM.value)
        self.assertFalse(instagram.available)
        self.assertEqual(instagram.reason, REASON_IG_PRO_REQUIRED)

    def test_instagram_requires_permissions(self):
        SocialAccount.objects.create(
            user=self.user,
            platform=Platform.INSTAGRAM,
            display_name='IG',
            account_type=SocialAccount.AccountType.INSTAGRAM_PROFESSIONAL,
            permissions_valid=False,
        )
        availability = evaluate_availability(self.user, 'TEXT', None)
        instagram = self._get_platform(availability, Platform.INSTAGRAM.value)
        self.assertFalse(instagram.available)
        self.assertEqual(instagram.reason, REASON_IG_PERMS_MISSING)

    def test_tiktok_photo_requires_prereqs(self):
        SocialAccount.objects.create(
            user=self.user,
            platform=Platform.TIKTOK,
            display_name='TT',
            tiktok_prerequisites_met=False,
            tiktok_photo_post_enabled=True,
        )
        availability = evaluate_availability(self.user, 'PHOTO', None)
        tiktok = self._get_platform(availability, Platform.TIKTOK.value)
        self.assertFalse(tiktok.available)
        self.assertEqual(tiktok.reason, REASON_TIKTOK_PREREQS)

    def test_x_media_requires_tier(self):
        SocialAccount.objects.create(
            user=self.user,
            platform=Platform.X,
            display_name='X',
            x_media_upload_enabled=False,
        )
        availability = evaluate_availability(self.user, 'PHOTO', None)
        x_platform = self._get_platform(availability, Platform.X.value)
        self.assertFalse(x_platform.available)
        self.assertEqual(x_platform.reason, REASON_X_MEDIA_DISABLED)

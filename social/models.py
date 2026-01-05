from django.conf import settings
from django.db import models


class Platform(models.TextChoices):
    INSTAGRAM = 'instagram', 'Instagram'
    FACEBOOK = 'facebook', 'Facebook'
    TIKTOK = 'tiktok', 'TikTok'
    YOUTUBE = 'youtube', 'YouTube'
    LINKEDIN = 'linkedin', 'LinkedIn'
    X = 'x', 'X'


class SocialAccount(models.Model):
    class AccountType(models.TextChoices):
        INSTAGRAM_PROFESSIONAL = 'instagram_professional', 'Instagram Professional'
        INSTAGRAM_PERSONAL = 'instagram_personal', 'Instagram Personal'
        FACEBOOK_PAGE = 'facebook_page', 'Facebook Page'
        FACEBOOK_PROFILE = 'facebook_profile', 'Facebook Profile'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=Platform.choices)
    display_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=64, choices=AccountType.choices, blank=True)
    permissions_valid = models.BooleanField(default=False)
    tiktok_photo_post_enabled = models.BooleanField(default=False)
    tiktok_prerequisites_met = models.BooleanField(default=False)
    linkedin_access_granted = models.BooleanField(default=False)
    x_media_upload_enabled = models.BooleanField(default=False)
    x_api_tier = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.platform}:{self.display_name}'

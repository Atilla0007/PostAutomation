from django.conf import settings
from django.db import models

from social.models import SocialAccount


class Post(models.Model):
    class ContentType(models.TextChoices):
        TEXT = 'TEXT', 'Text'
        PHOTO = 'PHOTO', 'Photo'
        VIDEO = 'VIDEO', 'Video'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=ContentType.choices)
    caption = models.TextField(blank=True)
    hashtags = models.JSONField(default=list, blank=True)
    image_file = models.FileField(upload_to='images/', null=True, blank=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    media_metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id}:{self.content_type}:{self.id}'


class PostTarget(models.Model):
    class Status(models.TextChoices):
        SELECTED = 'selected', 'Selected'
        QUEUED = 'queued', 'Queued'
        REJECTED = 'rejected', 'Rejected'
        PUBLISHED = 'published', 'Published'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='targets')
    social_account = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SELECTED)
    last_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'social_account')

    def __str__(self):
        return f'{self.post_id}:{self.social_account_id}:{self.status}'

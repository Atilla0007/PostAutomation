from rest_framework import serializers

from apps.posts.models import Post, PostTarget
from apps.integrations.models import SocialAccount


class DraftPostSerializer(serializers.Serializer):
    content_type = serializers.ChoiceField(choices=Post.ContentType.choices)
    caption = serializers.CharField(required=False, allow_blank=True)
    hashtags = serializers.ListField(child=serializers.CharField(), required=False)
    image_file = serializers.FileField(required=False, allow_null=True)
    video_file = serializers.FileField(required=False, allow_null=True)
    media_metadata = serializers.DictField(required=False)

    def validate(self, attrs):
        content_type = attrs.get('content_type')
        caption = attrs.get('caption')
        image_file = attrs.get('image_file')
        video_file = attrs.get('video_file')

        errors = {}
        if content_type == Post.ContentType.TEXT:
            if not caption:
                errors['caption'] = 'Caption is required for TEXT posts.'
            if image_file or video_file:
                errors['media'] = 'TEXT posts cannot include image or video files.'
        elif content_type == Post.ContentType.PHOTO:
            if not image_file:
                errors['image_file'] = 'Image file is required for PHOTO posts.'
            if video_file:
                errors['video_file'] = 'PHOTO posts cannot include video files.'
            if not caption:
                errors['caption'] = 'Caption is required for PHOTO posts.'
        elif content_type == Post.ContentType.VIDEO:
            if not video_file:
                errors['video_file'] = 'Video file is required for VIDEO posts.'
            if image_file:
                errors['image_file'] = 'VIDEO posts cannot include image files.'
            if not caption:
                errors['caption'] = 'Caption is required for VIDEO posts.'
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class PostSerializer(serializers.ModelSerializer):
    caption = serializers.CharField(required=True, allow_blank=False)
    target_account_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'content_type',
            'caption',
            'hashtags',
            'image_file',
            'video_file',
            'media_metadata',
            'target_account_ids',
        ]

    def validate(self, attrs):
        content_type = attrs.get('content_type') or getattr(self.instance, 'content_type', None)
        caption = attrs.get('caption')
        image_file = attrs.get('image_file')
        video_file = attrs.get('video_file')

        errors = {}
        existing_caption = getattr(self.instance, 'caption', None)
        if caption is None:
            caption = existing_caption

        if content_type == Post.ContentType.TEXT:
            if not caption:
                errors['caption'] = 'Caption is required for TEXT posts.'
            if image_file or video_file:
                errors['media'] = 'TEXT posts cannot include image or video files.'
        elif content_type == Post.ContentType.PHOTO:
            if image_file is None and not getattr(self.instance, 'image_file', None):
                errors['image_file'] = 'Image file is required for PHOTO posts.'
            if video_file:
                errors['video_file'] = 'PHOTO posts cannot include video files.'
            if not caption:
                errors['caption'] = 'Caption is required for PHOTO posts.'
        elif content_type == Post.ContentType.VIDEO:
            if video_file is None and not getattr(self.instance, 'video_file', None):
                errors['video_file'] = 'Video file is required for VIDEO posts.'
            if image_file:
                errors['image_file'] = 'VIDEO posts cannot include image files.'
            if not caption:
                errors['caption'] = 'Caption is required for VIDEO posts.'
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        target_ids = validated_data.pop('target_account_ids', [])
        post = Post.objects.create(user=self.context['request'].user, **validated_data)
        if target_ids:
            accounts = SocialAccount.objects.filter(id__in=target_ids, user=self.context['request'].user)
            for account in accounts:
                PostTarget.objects.create(post=post, social_account=account)
        return post

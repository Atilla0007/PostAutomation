from dataclasses import asdict

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.capabilities.services.availability_service import evaluate_availability
from apps.posts.models import Post, PostTarget
from apps.posts.serializers import PostSerializer
from apps.posts.tasks import publish_target


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-id')

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        availability = evaluate_availability(request.user, post.content_type, post.media_metadata)
        availability_by_account = {}
        for platform in availability:
            for account in platform.accounts:
                availability_by_account[account.social_account_id] = account

        queued = []
        rejected = []

        for target in PostTarget.objects.filter(post=post).select_related('social_account'):
            account_availability = availability_by_account.get(target.social_account_id)
            if not account_availability or not account_availability.available:
                reason = account_availability.reason if account_availability else 'Account not available for publishing.'
                target.status = PostTarget.Status.REJECTED
                target.last_error = reason
                target.save(update_fields=['status', 'last_error'])
                rejected.append({
                    'post_target_id': target.id,
                    'social_account_id': target.social_account_id,
                    'reason': reason,
                })
                continue
            target.status = PostTarget.Status.QUEUED
            target.last_error = ''
            target.save(update_fields=['status', 'last_error'])
            publish_target.delay(target.id)
            queued.append(target.id)

        payload = {
            'queued_post_target_ids': queued,
            'rejected': rejected,
            'availability': [asdict(item) for item in availability],
        }
        return Response(payload, status=status.HTTP_200_OK)

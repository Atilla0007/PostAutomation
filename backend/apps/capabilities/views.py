from dataclasses import asdict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.capabilities.services.availability_service import evaluate_availability
from apps.posts.models import Post
from apps.posts.serializers import DraftPostSerializer


class CapabilitiesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content_type = request.query_params.get('content_type')
        if content_type not in Post.ContentType.values:
            return Response({'detail': 'Invalid content_type.'}, status=status.HTTP_400_BAD_REQUEST)
        availability = evaluate_availability(request.user, content_type, None)
        return Response([asdict(item) for item in availability])


class CapabilitiesValidateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DraftPostSerializer(data=request.data)
        is_valid = serializer.is_valid()

        content_type = request.data.get('content_type')
        availability = []
        if content_type in Post.ContentType.values:
            availability = evaluate_availability(request.user, content_type, request.data.get('media_metadata'))

        if not is_valid:
            return Response(
                {'availability': [asdict(item) for item in availability], 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'availability': [asdict(item) for item in availability], 'errors': {}},
            status=status.HTTP_200_OK,
        )

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.posts.views import PostViewSet

router = DefaultRouter(trailing_slash=False)
router.register('', PostViewSet, basename='posts')

app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
]


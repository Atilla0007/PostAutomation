from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from capabilities.views import CapabilitiesValidateView, CapabilitiesView
from posts.views import PostViewSet

router = DefaultRouter(trailing_slash=False)
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('capabilities', CapabilitiesView.as_view(), name='capabilities'),
    path('capabilities/validate', CapabilitiesValidateView.as_view(), name='capabilities-validate'),
    path('', include(router.urls)),
]

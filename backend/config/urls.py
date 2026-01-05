from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/capabilities/', include('apps.capabilities.urls')),
    path('api/posts/', include('apps.posts.urls')),
]


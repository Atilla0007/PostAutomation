from django.contrib import admin
from apps.posts.models import Post, PostTarget


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content_type', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['caption', 'user__username']


@admin.register(PostTarget)
class PostTargetAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'social_account', 'status', 'created_at']
    list_filter = ['status', 'created_at']


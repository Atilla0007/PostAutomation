from django.contrib import admin
from apps.integrations.models import SocialAccount


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'platform', 'display_name', 'account_type', 'created_at']
    list_filter = ['platform', 'account_type', 'created_at']
    search_fields = ['display_name', 'user__username']


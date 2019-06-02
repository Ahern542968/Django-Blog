from django.contrib import admin

from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'like_object', 'created_at', 'updated_at']
    search_fields = ['like_object', 'user']
    list_filter = ['user', 'content_type', 'created_at', 'updated_at']
    list_per_page = 50



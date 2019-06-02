from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import Blog, Tag, Type
from .adminforms import BlogAdminForm


class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not obj.user.is_author and not obj.user.is_superuser:
            raise PermissionDenied
        return super().save_model(request, obj, form, change)


@admin.register(Blog)
class BlogAdmin(BaseAdmin):
    form = BlogAdminForm
    list_display = ['title', 'user', 'image', 'slug', 'status', 'type', 'content', 'get_like_num', 'created_at', 'updated_at']
    search_fields = ['title', 'tags', 'content']
    list_filter = ['user', 'status', 'tags', 'type', 'created_at', 'updated_at']
    list_per_page = 50
    ordering = ['-created_at']
    fields = ['title', 'image', 'status', 'type', 'tags', 'content']


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ['name', 'user', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['name', 'user']
    list_per_page = 50
    fields = ['name']


@admin.register(Type)
class TypeAdmin(BaseAdmin):
    list_display = ['name', 'user', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['name', 'user']
    list_per_page = 50
    fields = ['name']

import xadmin

from .models import Blog, Tag, Type
from .adminforms import BlogAdminForm


class BlogAdmin(object):
    form = BlogAdminForm
    list_display = ['title', 'author', 'image', 'slug', 'status', 'tags', 'btype', 'content', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    list_filter = ['author', 'status', 'tags', 'btype']


class TagAdmin(object):
    list_display = ['name', 'author', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['name', 'author']


class TypeAdmin(object):
    list_display = ['name', 'author', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['name', 'author']


xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Type, TypeAdmin)

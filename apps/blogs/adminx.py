import xadmin

from .models import Blog, BlogTag, BlogType


class BlogAdmin(object):
    list_display = ['id', 'author', 'blog_type', 'blog_tag', 'title', 'content', 'created_date', 'updated_date']
    search_fields = ['id', 'author', 'blog_type', 'blog_tag', 'title', 'content', 'created_date']
    list_filter = ['author', 'blog_type', 'blog_tag']


class BlogTagAdmin(object):
    list_display = ['id', 'name', 'created_date', 'updated_date']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


class BlogTypeAdmin(object):
    list_display = ['id', 'name', 'created_date', 'updated_date']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(BlogTag, BlogTagAdmin)
xadmin.site.register(BlogType, BlogTypeAdmin)


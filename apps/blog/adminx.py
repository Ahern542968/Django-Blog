import xadmin

from .models import Blog, BlogTag, BlogType


class BlogAdmin(object):
    list_display = ['id', 'author', 'blog_type', 'blog_tag', 'title', 'content', 'date']
    search_fields = ['id', 'author', 'blog_type', 'blog_tag', 'title', 'content']
    list_filter = ['author', 'blog_type', 'blog_tag']
    fields = ['blog_type', 'blog_tag', 'title', 'content']
    # filter_horizontal = ['blog_tag']
    # date_hierarchy = 'date'


class BlogTagAdmin(object):
    list_display = ['id', 'name', 'date']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


class BlogTypeAdmin(object):
    list_display = ['id', 'name', 'date']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(BlogTag, BlogTagAdmin)
xadmin.site.register(BlogType, BlogTypeAdmin)


import xadmin

from .models import Blog, BlogTag, BlogType
from .adminforms import BlogAdminForm


class BlogAdmin(object):
    form = BlogAdminForm
    list_display = ['id', 'author', 'blog_type', 'blog_tag', 'title', 'content',
                    'like_num', 'views', 'comms', 'date', 'is_top']
    search_fields = ['id', 'author', 'blog_type', 'blog_tag', 'title', 'content', 'is_top']
    list_filter = ['author', 'blog_type', 'blog_tag', 'is_top']
    fields = ['blog_type', 'blog_tag', 'title', 'author', 'content', 'is_top']
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


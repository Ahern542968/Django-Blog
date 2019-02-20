import xadmin

from .models import Comment


class CommentAdmin(object):
    list_display = ['id', 'blog', 'user', 'content', 'is_active', 'date']
    search_fields = ['id', 'blog', 'user', 'content', 'is_active']
    list_filter = ['blog', 'user', 'content', 'is_active']


xadmin.site.register(Comment, CommentAdmin)

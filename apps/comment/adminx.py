import xadmin

from .models import Comment


class CommentAdmin(object):
    list_display = ['id', 'blog', 'c_user', 'content', 'status', 'r_comment', 'p_comment', 'r_user', 'date']
    search_fields = ['id', 'blog', 'c_user', 'content', 'status', 'r_comment', 'p_comment', 'r_user']
    list_filter = ['blog', 'c_user', 'content', 'status', 'r_comment', 'p_comment', 'r_user']


xadmin.site.register(Comment, CommentAdmin)

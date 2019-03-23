from django.db import models
from django.contrib.auth import get_user_model

from blog.models import Blog
from utils.lrucache import redis_cache
# Create your models here.

User = get_user_model()


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='博客')
    content = models.CharField(max_length=300, verbose_name='内容')
    c_user = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE, verbose_name='评论')
    r_comment = models.ForeignKey('self', related_name='root_comment', null=True, blank=True,
                                  on_delete=models.CASCADE, verbose_name='根评论')
    p_comment = models.ForeignKey('self', related_name='parent_comment', null=True, blank=True,
                                  on_delete=models.CASCADE, verbose_name='父评论')
    r_user = models.ForeignKey(User, related_name='reply_user', null=True, blank=True,
                               on_delete=models.CASCADE, verbose_name='回复')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.content

    @classmethod
    @redis_cache('latest_comments', 60 * 60 * 5)
    def get_latest_comments(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-date')[:5]

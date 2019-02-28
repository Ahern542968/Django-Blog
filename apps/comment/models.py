from django.db import models
from django.contrib.auth import get_user_model

from blog.models import Blog
# Create your models here.

User = get_user_model()


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='博客')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    content = models.CharField(max_length=300, verbose_name='内容')
    # parent_com = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父评论')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return 'content by {} on {}'.format(self.user, self.blog)


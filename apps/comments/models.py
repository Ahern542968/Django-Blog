import uuid

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class CommentQuerySet(models.query.QuerySet):
    """自定义标签QuerySet, 提高模型的可用性"""
    def get_comment_num(self, content_type, object_id):
        return self.filter(content_type=content_type, object_id=object_id).count()

    def get_reply(self):
        return self.filter(reply=True)


class Comment(models.Model):
    """使用Django中的ContentType，便于数据分析"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commentator', on_delete=models.CASCADE, verbose_name='用户')
    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="like_on", on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50, blank=True, null=True)
    comment_object = GenericForeignKey("content_type", "object_id")  # 或GenericForeignKey()
    content = models.TextField('评论内容')

    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, verbose_name='父评论')
    root = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="thread", verbose_name='根评论')
    reply = models.BooleanField('是否为回复', default=False)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    objects = CommentQuerySet.as_manager()

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        index_together = ("content_type", "object_id")  # 联合唯一索引
        unique_together = ("user", "content_type", "object_id")  # 联合唯一键

    def __str__(self):
        return self.content

    def get_parent(self):
        return self.parent if self.parent else self

    def get_root(self):
        return self.parent.root if self.parent else self

    def reply_this(self, content_type, object_id, user, text):
        """
        新的回复
        :param content_type:    评论回复的对象
        :param object_id:       评论回复对象的id
        :param user:            评论人
        :param text:            内容
        :return:                None
        """
        parent = self.get_parent()
        root = self.get_root()
        reply_news = Comment.objects.create(
            content_type=content_type,
            user=user,
            object_id=object_id,
            content=text,
            reply=True,
            parent=parent,
            root=root
        )

    def get_thread(self):
        self.refresh_from_db()
        return self.root.thread.get_reply()

    def get_reply_num(self):
        return self.get_thread().count()

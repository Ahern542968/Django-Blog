import uuid

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class LikeQuerySet(models.query.QuerySet):
    """自定义标签QuerySet, 提高模型的可用性"""
    def count_like(self, content_type, object_id):
        return self.filter(content_type=content_type, object_id=object_id).count()


class Like(models.Model):
    """使用Django中的ContentType，便于数据分析"""
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name="like_on", on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50, blank=True, null=True)
    like_object = GenericForeignKey("content_type", "object_id")  # 或GenericForeignKey()
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    objects = LikeQuerySet.as_manager()

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
        index_together = ("content_type", "object_id")  # 联合唯一索引
        unique_together = ("user", "content_type", "object_id")  # 联合唯一键

    def __str__(self):
        return self.user.get_name()


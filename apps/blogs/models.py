from collections import defaultdict

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.shortcuts import reverse

from uuslug import slugify

from users.models import User
from likes.models import Like
# Create your models here.


class TagQuerySet(models.query.QuerySet):
    """自定义标签QuerySet, 提高模型的可用性"""
    def names(self):
        return [tag.name for tag in self.all()]


class Tag(models.Model):
    name = models.CharField('标签', max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', related_name='tag_author', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    objects = TagQuerySet.as_manager()

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField('分类', max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='type_author', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BlogQuerySet(models.query.QuerySet):
    """自定义博客QuerySet, 提高模型的可用性"""
    def get_publish(self, tag=None):
        return self.filter(status='publish', tags__name=tag) if tag else self.filter(status='publish')

    def get_tags_cloud(self):
        """统计所有已发布的博客中，每一个标签的数量(大于0的)"""
        tag_dict = defaultdict(int)
        for obj in self.get_publish():
            for tag in obj.tags.all().names():
                tag_dict[tag] += 1
        return tag_dict.items()


class Blog(models.Model):
    STATUS = (('publish', '发布'), ('draft', '草稿'), ('delete', '删除'), ('diary', '日记'))
    title = models.CharField('标题', max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_author', verbose_name='作者', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField('图片', upload_to='blog_imgs/%Y/%m/%d/', null=True, blank=True)
    slug = models.SlugField('(URL)别名', max_length=255, null=True, blank=True)
    status = models.CharField('状态', choices=STATUS, default='draft', max_length=10)
    content = models.TextField('内容')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    type = models.ForeignKey(Type, related_name='blog_type', verbose_name='分类', null=True, blank=True, on_delete=models.SET_NULL)
    likes = GenericRelation(Like, verbose_name='点赞情况')  # 通过GenericRelation关联到Like表，不是实际的字段
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    objects = BlogQuerySet.as_manager()

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super().save()

    def get_like_num(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={'slug': self.slug})


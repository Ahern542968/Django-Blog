from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import F

from utils.lrucache import redis_cache

# Create your models here.

User = get_user_model()


class BlogType(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_HIDDEN = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_HIDDEN, '隐藏'),
    )

    name = models.CharField(max_length=15, verbose_name='博客分类')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Mate:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_HIDDEN = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_HIDDEN, '隐藏'),
    )
    name = models.CharField(max_length=15, verbose_name='博客标签')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Mate:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_blog_num(self):
        return self.blog_set.all().count()


class Blog(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )
    author = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    blog_type = models.ForeignKey(BlogType, verbose_name='分类', on_delete=models.CASCADE)
    blog_tag = models.ManyToManyField(BlogTag, verbose_name='标签')
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_top = models.BooleanField(default=False, verbose_name='是否推荐')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    like_num = models.IntegerField(default=0, verbose_name='点赞数量')
    views = models.IntegerField(default=0, verbose_name='阅读数量')
    comms = models.IntegerField(default=0, verbose_name='评论数量')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Mate:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name
        ordering = ['-date']

    def __str__(self):
        return self.title

    def tags(self):
        return ', '.join(self.blog_tag.values_list('name', flat=True))

    def add_views(self):
        self.__class__.objects.filter(pk=self.id).update(views=F('views') + 1)

    def add_comms(self):
        self.__class__.objects.filter(pk=self.id).update(comms=F('comms') + 1)

    @classmethod
    @redis_cache('blog_num', 60*60*5)
    def get_blog_num(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).count()

    @classmethod
    @redis_cache('topped_blogs', 60*60*5)
    def get_topped_blogs(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL, is_top=True)[:5].only('title', 'id')

    @classmethod
    @redis_cache('latest_blogs', 60*60*5)
    def get_latest_blogs(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-date')[:5].only('title', 'id')

    def get_absolute_url(self):
        return reverse('blog:blog-detail', args=[str(self.id)])

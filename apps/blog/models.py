from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class BlogType(models.Model):
    name = models.CharField(max_length=15, verbose_name='博客分类')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Mate:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BlogTag(models.Model):
    name = models.CharField(max_length=15, verbose_name='博客标签')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Mate:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    author = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    blog_type = models.ForeignKey(BlogType, verbose_name='分类', on_delete=models.CASCADE)
    blog_tag = models.ManyToManyField(BlogTag, verbose_name='标签')
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_top = models.BooleanField(default=False, verbose_name='是否推荐')
    like_num = models.IntegerField(default=0, verbose_name='点赞数量')
    read_num = models.IntegerField(default=0, verbose_name='阅读数量')
    comm_num = models.IntegerField(default=0, verbose_name='评论数量')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Mate:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

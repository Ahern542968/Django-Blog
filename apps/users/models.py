from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    ROLE = (('author', '作者'), ('guest', '访客'))
    role = models.CharField('角色', choices=ROLE, default='guest', max_length=6)
    nickname = models.CharField('昵称', max_length=32, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avator/', null=True, blank=True)
    position = models.CharField('职位', max_length=32, null=True, blank=True)
    work_year = models.CharField('工作年限', max_length=32, null=True, blank=True)
    personal_url = models.URLField('个人链接', max_length=128, null=True, blank=True)
    github_url = models.URLField('GitHub链接', max_length=128, null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self.nickname if self.nickname else self.username

    @property
    def is_author(self):
        return self.role == 'author'

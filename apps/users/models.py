from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=32, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avator/', null=True, blank=True)
    position = models.CharField('职位', max_length=32, null=True, blank=True)
    work_year = models.CharField('工作年限', max_length=32, null=True, blank=True)
    personal_url = models.URLField('个人链接', max_length=128, null=True, blank=True)
    github_url = models.URLField('GitHub链接', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = '个人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return self.nickname if self.nickname else self.username


class Author(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '作者信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author.get_name()

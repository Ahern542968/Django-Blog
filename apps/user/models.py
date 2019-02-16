from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=15, null=True, blank=True, verbose_name='昵称')
    email = models.EmailField(max_length=50, unique=True, verbose_name='邮箱')
    is_active = models.BooleanField(default=False, verbose_name='是否激活')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Mate:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

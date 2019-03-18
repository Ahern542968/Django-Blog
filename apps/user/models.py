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

    @property
    def get_name(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username


class UserActiveCode(models.Model):
    FOR_BLIND_EMAIL = 0
    FOR_FORGET_PASSWORD = 1
    SEND_FOR = (
        (FOR_BLIND_EMAIL, '绑定邮箱'),
        (FOR_FORGET_PASSWORD, '忘记密码'),
    )
    send_for = models.CharField(max_length=20, choices=SEND_FOR, verbose_name='发送')
    email = models.CharField(max_length=128, verbose_name='邮箱')
    code = models.CharField(max_length=56, verbose_name='激活码')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Mate:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name
        ordering = ['-date']

    def __str__(self):
        return '%s %s 验证码 %s' % (self.email, self.send_for, self.code)



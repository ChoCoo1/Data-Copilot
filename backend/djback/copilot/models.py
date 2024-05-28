from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
# 用户表
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, blank=True)  # 添加手机号字段
    created_at = models.DateTimeField(default=timezone.now)  # 添加创建时间字段，自动填充当前时间

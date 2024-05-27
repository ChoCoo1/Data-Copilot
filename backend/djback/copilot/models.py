from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# 用户表
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)  # 添加手机号字段
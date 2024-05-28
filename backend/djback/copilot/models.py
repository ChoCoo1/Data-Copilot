from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.
# 用户表
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, blank=True)  # 添加手机号字段
    created_at = models.DateTimeField(default=timezone.now)  # 添加创建时间字段，自动填充当前时间


class Database(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sql_type = models.CharField(max_length=50)
    sql_name = models.CharField(max_length=100)
    sql_port = models.IntegerField()
    sql_address = models.CharField(max_length=100)
    sql_login_name = models.CharField(max_length=100)
    sql_pwd = models.CharField(max_length=100)

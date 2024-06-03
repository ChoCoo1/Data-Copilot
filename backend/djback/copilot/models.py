from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
# 用户表
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, blank=True)  # 添加手机号字段
    created_at = models.DateTimeField(default=timezone.now)  # 添加创建时间字段，自动填充当前时间


class DatabaseConnection(models.Model):
    username = models.CharField(max_length=100, blank=True)
    sql_type = models.CharField(max_length=100, blank=True)
    sql_address = models.CharField(max_length=100, blank=True)
    sql_port = models.IntegerField(blank=True)
    sql_login_name = models.CharField(max_length=100, blank=True)
    sql_pwd = models.CharField(max_length=100, blank=True)
    sql_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Database Connection for {self.username}"

    def all_valid(self):
        try:
            self.full_clean()
        except ValidationError as e:
            return False, e.message_dict
        return True, None


class SearchHistory(models.Model):
    username = models.CharField(max_length=100, blank=True)
    search_query = models.CharField(max_length=255, blank=True)
    search_sql_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    username_validator = RegexValidator(
        regex = r'^[a-zA-Z0-9_]+$',  # 允许的字符：字母、数字和下划线
        message = "用户名只能包含英文字母, 数字以及下划线"
    )
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[username_validator] # 添加验证器
    )
    stats_rps_win = models.IntegerField(default=0)
    stats_rps_lose = models.IntegerField(default=0)

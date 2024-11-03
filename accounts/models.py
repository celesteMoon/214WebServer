from django.db import models

from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    # username
    username_validator = RegexValidator(
        regex = r'^[a-zA-Z0-9_]+$',
        message = "用户名只能包含英文字母, 数字以及下划线"
    )
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[username_validator]
    )

    # custom colour
    # color_validator = RegexValidator(
    #     regex = r'^[#]{1}[A-F0-9a-f]{6}$', 
    #     message = "请输入合法的十六进制六位数"
    # )
    background_color = models.CharField(max_length=7, default="#FFFFFF")

    # stats
    stats_rps_win = models.IntegerField(default=0)
    stats_rps_lose = models.IntegerField(default=0)
    # stats_rps_winstreak = models.IntegerField(default=0)
    # stats_rps_maxwinstreak = models.IntegerField(default=0)

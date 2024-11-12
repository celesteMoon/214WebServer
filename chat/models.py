import os, sys, django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 将配置文件的路径写到django_settings_module环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "214web.settings")
django.setup()

from django.db import models
from django.utils import timezone

# Create your models here.

class Message(models.Model):
    username = models.CharField(max_length=20)
    message = models.TextField()
    # time = models.DateTimeField(default=timezone.now)
    time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        if Message.objects.count() > 100:
            oldest = Message.objects.order_by("time").first()
            oldest.delete()

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return f'[{self.time}]{self.username}: {self.message}'
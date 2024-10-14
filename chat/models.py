from django.db import models
from django.utils import timezone

# Create your models here.

class Message(models.Model):
    username = models.CharField(max_length=100)
    content = models.TextField()
    # timestamp = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.timestamp}]{self.username}: {self.content}'
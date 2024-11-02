from channels.generic.websocket import WebsocketConsumer
import os, sys, django, json, logging

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 将配置文件的路径写到django_settings_module环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "214web.settings")
django.setup()

from .models import CustomUser
from django.utils import timezone
from django.template.defaultfilters import date

logger = logging.getLogger('accounts/consumers.py')

class ProfileConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.accept()
        text_data = self.get_user(self.username)
        if text_data is not None:
            self.send(text_data=text_data)
        else:
            self.send(text_data=json.dumps({'error': 'error'}))

    def disconnect(self, code):
        return super().disconnect(code)
    
    def receive(self, text_data=None, bytes_data=None):
        return super().receive(text_data, bytes_data)

    def get_user(self, username):
        if not CustomUser.objects.filter(username=username).exists():
            return None
        user = CustomUser.objects.get(username=username)
        return json.dumps({
            'username': user.username,
            'join_date': date(timezone.localtime(user.date_joined), "Y M jS H:i:s O"),
            'rps_win': user.stats_rps_win,
            'rps_lose': user.stats_rps_lose,
        })
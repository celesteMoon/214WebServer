import os, sys, django, json, logging

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# 将配置文件的路径写到django_settings_module环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "214web.settings")
django.setup()

from channels.generic.websocket import WebsocketConsumer
from accounts.models import CustomUser

logger = logging.getLogger('user_setting/consumers.py')

class SettingConsumer(WebsocketConsumer):
    def connect(self):
        return super().connect()

    def disconnect(self, code):
        return super().disconnect(code)
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        # user = CustomUser.objects.get(username=self.scope["user"].username)
        user = self.scope["user"]
        user.background_color = text_data_json["background_color"]
        user.save()
        # logger.info(user.username + ": " + user.background_color)

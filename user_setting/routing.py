from django.urls import path
from . import consumers

user_setting_urlpatterns = [
    path('ws/setting/', consumers.SettingConsumer.as_asgi())
]

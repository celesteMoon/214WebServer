from django.urls import path, re_path
from . import consumers

rps_urlpatterns = [
    # path('ws/game/', consumers.RPSConsumer.as_asgi()),
    re_path(r'ws/game/(?P<game_id>\w+)/$', consumers.RPSConsumer.as_asgi()),
]

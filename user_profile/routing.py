from django.urls import path, re_path
from . import consumers

user_profile_urlpatterns = [
    # path('ws/game/', consumers.RPSConsumer.as_asgi()),
    re_path(r'ws/profile/(?P<username>\w+)/$', consumers.ProfileConsumer.as_asgi()),
]

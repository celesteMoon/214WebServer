from django.urls import path
from . import consumers

rps_urlpatterns = [
    path('ws/game/', consumers.RPSConsumer.as_asgi()),
]

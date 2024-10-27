from django.urls import path
from .views import game_view, lobby_view

urlpatterns = [
    path('', lobby_view, name='lobby'),
    path('game/', game_view, name='rps'),
]
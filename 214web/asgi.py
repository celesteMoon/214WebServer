"""
ASGI config for 214web project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.routing import chat_urlpatterns
from rps.routing import rps_urlpatterns
from user_profile.routing import user_profile_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '214web.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_urlpatterns + rps_urlpatterns + user_profile_urlpatterns
        )
    ),
})

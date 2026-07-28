"""
ASGI config for chatapp project.
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack

from chat.routing import websocket_urlpatterns


print("ASGI LOADED")


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({

    "http": django_asgi_app,

    "websocket": SessionMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),

})
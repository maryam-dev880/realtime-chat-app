from django.urls import path
from .consumers import ChatConsumer

print("ROUTING FILE LOADED")

websocket_urlpatterns = [
    path("ws/chat/<room_name>/", ChatConsumer.as_asgi()),
]
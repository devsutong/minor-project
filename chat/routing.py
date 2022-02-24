from django.urls import re_path

from .consumers import SocketConsumer

websocket_urlpatterns = [
    re_path(r"socket/$", SocketConsumer.as_asgi()),
]
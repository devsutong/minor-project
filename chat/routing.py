# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from .consumers import SocketConsumer
# from .token_auth import JwtAuthMiddlewareStack

# from django.core.asgi import get_asgi_application
# from channels.security.websocket import AllowedHostsOriginValidator

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": JwtAuthMiddlewareStack(
#                 URLRouter(
#                     [
#                         path("socket/", SocketConsumer.as_asgi()),
#                     ]
#                 )
#             ),
#     }
# )

from django.urls import re_path

from .consumers import SocketConsumer

websocket_urlpatterns = [
    re_path(r"socket/$", SocketConsumer.as_asgi()),
]
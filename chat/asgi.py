import os
# import django
# from django.conf import settings
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .token_auth import JwtAuthMiddlewareStack
from . import routing

# settings.configure()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minorproject.settings")
# django.setup()

# settings.configure()
application = application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JwtAuthMiddlewareStack(
                URLRouter(routing.websocket_urlpatterns)
            ),
    }
)


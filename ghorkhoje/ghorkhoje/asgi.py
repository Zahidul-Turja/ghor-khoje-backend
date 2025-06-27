import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ghorkhoje.settings")
django.setup()  # <-- Initialize Django apps before any model-related imports

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from ghorkhoje.routing import websocket_urlpatterns
from ghorkhoje.middlewares import ChatAuthMiddleware

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            ChatAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)

# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
#         ),
#     }
# )

from django.urls import re_path

from chat.consumers import ChatConsumer
from ghorkhoje.middlewares import ChatAuthMiddleware

websocket_urlpatterns = [
    re_path(r"ws/chat/", ChatAuthMiddleware(ChatConsumer.as_asgi())),
]

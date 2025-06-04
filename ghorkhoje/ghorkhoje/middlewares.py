from urllib.parse import parse_qs
import jwt
import json
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from channels.auth import AuthMiddlewareStack
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


class ChatAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()

        query_params = parse_qs(scope["query_string"].decode("utf8"))

        token = query_params.get("token", [None])[0]

        if token:
            try:
                decoded_data = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                user = await database_sync_to_async(get_user_model().objects.get)(
                    id=decoded_data["user_id"]
                )
                scope["user"] = user
                scope["is_agent"] = user.is_staff or user.is_superuser
            except jwt.ExpiredSignatureError:
                return None
            except jwt.InvalidTokenError:
                return None
        else:
            scope["user"] = None
            scope["is_agent"] = False

        return await self.app(scope, receive, send)

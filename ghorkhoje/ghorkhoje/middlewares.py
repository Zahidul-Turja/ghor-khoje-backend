from urllib.parse import parse_qs
import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections


class ChatAuthMiddleware:
    def __init__(self, app):  # <- correct init method name
        self.app = app

    async def __call__(self, scope, receive, send):  # <- correct __call__ method
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
                scope["is_admin"] = user.is_staff or user.is_superuser
            except jwt.ExpiredSignatureError:
                scope["user"] = None
            except jwt.InvalidTokenError:
                scope["user"] = None
        else:
            scope["user"] = None
            scope["is_admin"] = False

        return await self.app(scope, receive, send)

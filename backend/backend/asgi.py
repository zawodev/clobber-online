# backend/asgi.py
import os
from django.core.asgi import get_asgi_application
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user_for_token(token_key):
    try:
        return Token.objects.get(key=token_key).user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    """
    ASGI middleware: czyta ?token=<klucz> z querystring i ustawia scope['user'].
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # parsujemy querystring
        query_string = scope.get("query_string", b"").decode()
        qs = parse_qs(query_string)
        token_key = qs.get("token", [None])[0]

        if token_key:
            scope["user"] = await get_user_for_token(token_key)
        else:
            scope["user"] = AnonymousUser()

        # wywołujemy dalszy ASGI-pipeline
        return await self.app(scope, receive, send)


import chat.routing, game.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns +
                game.routing.websocket_urlpatterns
            )
        )
    ),
})

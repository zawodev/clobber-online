from django.urls import re_path
from .consumers import GlobalChatConsumer, RoomChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/global/$', GlobalChatConsumer.as_asgi()),
    re_path(r'ws/chat/room/(?P<code>\w{6})/$', RoomChatConsumer.as_asgi()),
]

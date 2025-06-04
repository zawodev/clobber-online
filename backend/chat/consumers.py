import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from rooms.models import Room

class GlobalChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = "global_chat"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, data):
        user = self.scope['user']
        msg = data.get('message')
        if not msg or not user.is_authenticated:
            return

        await database_sync_to_async(ChatMessage.objects.create)(
            user=user, content=msg, room=None
        )

        await self.channel_layer.group_send(
            self.group_name,
            {"type": "chat.message", "user": user.username, "message": msg}
        )

    async def chat_message(self, event):
        await self.send_json({
            "user": event["user"],
            "message": event["message"]
        })


class RoomChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.code = self.scope['url_route']['kwargs']['code']
        self.group_name = f"room_chat_{self.code}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, data):
        user = self.scope['user']
        msg = data.get('message')
        if not msg or not user.is_authenticated:
            return
        room = await database_sync_to_async(Room.objects.get)(code=self.code)
        await database_sync_to_async(ChatMessage.objects.create)(
            user=user, content=msg, room=room
        )
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "chat.message", "user": user.username, "message": msg}
        )

    async def chat_message(self, event):
        await self.send_json({
            "user": event["user"],
            "message": event["message"]
        })

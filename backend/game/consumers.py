import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Game
from rooms.models import Room

User = get_user_model()

class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.code = self.scope['url_route']['kwargs']['code']
        self.group_name = f"game_{self.code}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        action = content.get('action')
        user = self.scope['user']
        if action == 'join':
            # inicjalizacja gry w momencie dołączenia drugiego gracza
            await self.init_game(user)
        elif action == 'move':
            frm, to = content['from'], content['to']
            await self.handle_move(user, frm, to)

    async def init_game(self, user):
        # załóżmy, że gra powstaje dopiero, gdy host + drugi grający są w pokoju
        room = await database_sync_to_async(Room.objects.get)(code=self.code)
        game, created = await database_sync_to_async(Game.objects.get_or_create)(
            room=room,
            defaults={'board': self.empty_board(room), 'current': room.host}
        )
        if created:
            game.board = self.empty_board(room)
            game.status = 'playing'
            await database_sync_to_async(game.save)()
        await self.group_send_state()

    def empty_board(self, room):
        return [[0]*room.width for _ in range(room.height)]

    async def handle_move(self, user, frm, to):
        game = await database_sync_to_async(Game.objects.get)(room__code=self.code)
        if game.status != 'playing' or game.current != user:
            return
        # walidacja ruchu...
        # zaktualizuj game.board, zmień game.current, sprawdź zwycięstwo
        await database_sync_to_async(game.save)()
        await self.group_send_state()

    async def group_send_state(self):
        game = await database_sync_to_async(Game.objects.get)(room__code=self.code)
        await self.channel_layer.group_send(
            self.group_name,
            {'type': 'game.state', 'board': game.board,
             'current': game.current.username, 'status': game.status}
        )

    async def game_state(self, event):
        await self.send_json({
            'board': event['board'],
            'current': event['current'],
            'status': event['status']
        })

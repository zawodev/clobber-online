import random
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Game, GameResult
from rooms.models import Room
from django.utils import timezone

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
            await database_sync_to_async(self._init_game)(user)
            await self.group_send_state()
        elif action == 'move':
            frm, to = tuple(content['from']), tuple(content['to'])
            moved = await database_sync_to_async(self._handle_move)(user, frm, to)
            if moved:
                await self.group_send_state(
                    last_move={'player': user.username, 'from': frm, 'to': to}
                )
            else:
                await self.group_send_state()  # nie nadpisujemy last_move przy invalid move (niby można? idk)

    def _init_game(self, user):
        room = Room.objects.get(code=self.code)
        room.players.add(user)
        game, created = Game.objects.get_or_create(
            room=room,
            defaults={
                'board': self._make_initial_board(room),
                'current': None,
                'status': 'waiting'
            }
        )
        players = list(room.players.all())
        if game.status != 'playing' and (len(players) == 2 or room.vs_ai):

            if room.challenge:
                game.board = room.challenge.board
            else:
                game.board = self._make_initial_board(room)

            game.status = 'playing'
            # game.current = room.host
            if room.creator_color == 'black':
                game.current = room.host
            else:
                opponent = next(p for p in players if p != room.host)
                game.current = opponent
            game.save()

    def _make_initial_board(self, room):
        h, w = room.height, room.width
        return [
            ['b' if (r + c) % 2 == 0 else 'w' for c in range(w)]
            for r in range(h)
        ]

    def _handle_move(self, user, frm, to):
        room = Room.objects.get(code=self.code)
        game = Game.objects.get(room=room)
        if game.status != 'playing' or game.current != user:
            return False

        board = game.board
        h, w = room.height, room.width

        # sprawdzenie granic i kierunku
        if not (0 <= frm[0] < h and 0 <= frm[1] < w and
                0 <= to[0] < h and 0 <= to[1] < w):
            return False
        user_color = 'b' if user == room.host else 'w'
        me = board[frm[0]][frm[1]]
        tgt = board[to[0]][to[1]]
        dr, dc = abs(frm[0] - to[0]), abs(frm[1] - to[1])
        if me != user_color or tgt is None or tgt == user_color or (dr+dc) != 1:
            return False

        # bicie
        board[to[0]][to[1]] = me
        board[frm[0]][frm[1]] = None

        players = list(room.players.all())
        if room.vs_ai:
            next_user = None
        else:
            next_user = players[0] if players[1] == user else players[1]
        game.current = next_user

        # koniec gry?
        if not self._has_any_move(board, game.current, room):
            game.status = 'finished'
            game.winner = user
            loser = players[0] if players[1] == user else players[1]
            GameResult.objects.create(game=game, winner=user, loser=loser)
            game.current = None
            user.wins += 1
            loser.losses += 1
            user.save()
            loser.save()

        game.board = board
        game.save()

        # ruch AI (NOT IMPLEMENTED)
        if room.vs_ai and game.status == 'playing':
            self._do_ai_move(game, room)

        return True

    def _has_any_move(self, board, user, room):
        if user is None:
            return False
        color = 'b' if user == room.host else 'w'
        for r in range(room.height):
            for c in range(room.width):
                if board[r][c] == color:
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        rr, cc = r+dr, c+dc
                        if 0 <= rr < room.height and 0 <= cc < room.width:
                            if board[rr][cc] not in (None, color):
                                return True
        return False

    def _do_ai_move(self, game, room):
        board = game.board
        ai_color = 'w' if room.creator_color == 'black' else 'b'
        moves = []
        for r in range(room.height):
            for c in range(room.width):
                if board[r][c] == ai_color:
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        rr, cc = r+dr, c+dc
                        if 0 <= rr < room.height and 0 <= cc < room.width:
                            if board[rr][cc] not in (None, ai_color):
                                moves.append(((r, c), (rr, cc)))
        if not moves:
            game.status = 'finished'
            game.winner = game.current
            GameResult.objects.create(
                game=game,
                winner=game.current,
                loser=room.host  # jeśli AI wygrywa host jest przegranym
            )
            # po ai nawet nie wrzucam winratu bo nie ma co
            game.current = None
            game.save()
            return

        frm, to = random.choice(moves)
        board[to[0]][to[1]] = ai_color
        board[frm[0]][frm[1]] = None
        game.current = room.host
        game.board = board
        game.save()

    async def group_send_state(self, last_move=None):
        data = await database_sync_to_async(self._get_state_data)(last_move)
        event = {'type': 'game_state', **data}
        await self.channel_layer.group_send(self.group_name, event)

    def _get_state_data(self, last_move):
        room = Room.objects.get(code=self.code)
        game = Game.objects.get(room=room)
        mapped = [
            [cell if cell in ('b', 'w') else '_' for cell in row]
            for row in game.board
        ]

        if game.current:
            if game.current == room.host:
                current_color = room.creator_color
            else:
                current_color = 'white' if room.creator_color == 'black' else 'black'
        else:
            current_color = None

        return {
            #'current': game.current.username if game.current else None,
            'current': current_color,
            'status': game.status,
            'last_move': last_move,
            'winner': game.winner.username if game.winner else None,
            'board': mapped,
        }

    async def game_state(self, event):
        resp = {
            'type': 'state',
            'current': event['current'],
            'status': event['status'],
            'last_move': event['last_move'],
            'winner': event.get('winner'),
            'board': event['board'],
        }
        await self.send_json(resp)


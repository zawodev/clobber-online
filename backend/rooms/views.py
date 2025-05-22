# rooms/views.py
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import RoomSerializer, JoinRoomSerializer
import random
import string

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def rooms(request):
    if request.method == 'POST':
        # Tylko zalogowani użytkownicy mogą utworzyć pokój
        # Generujemy unikalne 6-znakowe ID (wielkie litery i cyfry)
        while True:
            room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if cache.get(f"room_{room_id}") is None:
                break
        # Tworzymy strukturę pokoju: właściciel oraz uczestnik (początkowo tylko właściciel)
        room_data = {
            'id': room_id,
            'owner': request.user.username,
            'participants': [request.user.username]
        }
        # Zapis do cache (bez czasu wygaśnięcia)
        cache.set(f"room_{room_id}", room_data, timeout=None)
        # Dodanie ID do listy aktywnych pokoi
        rooms_list = cache.get('rooms', [])
        rooms_list.append(room_id)
        cache.set('rooms', rooms_list, timeout=None)
        return Response(RoomSerializer(room_data).data)

    else:
        # GET: lista aktywnych pokoi (dostępne dla każdego)
        rooms_list = cache.get('rooms', [])
        all_rooms = []
        for rid in rooms_list:
            data = cache.get(f"room_{rid}")
            if data:
                all_rooms.append(data)
        return Response(RoomSerializer(all_rooms, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_room(request):
    # Tylko zalogowani mogą dołączyć do pokoju
    serializer = JoinRoomSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    room_id = serializer.validated_data['room_id']
    room_key = f"room_{room_id}"
    room_data = cache.get(room_key)
    if not room_data:
        return Response({'detail': 'Pokój o podanym ID nie istnieje.'}, status=404)
    if request.user.username in room_data['participants']:
        return Response({'detail': 'Już jesteś w pokoju.'}, status=400)
    if len(room_data['participants']) >= 2:
        return Response({'detail': 'Pokój jest już pełny.'}, status=400)
    # Dodajemy użytkownika do pokoju
    room_data['participants'].append(request.user.username)
    cache.set(room_key, room_data, timeout=None)
    return Response(RoomSerializer(room_data).data)

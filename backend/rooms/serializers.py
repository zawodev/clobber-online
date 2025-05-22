# rooms/serializers.py
from rest_framework import serializers

class RoomSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=6)
    owner = serializers.CharField()              # nazwa użytkownika właściciela pokoju
    participants = serializers.ListField(
        child=serializers.CharField(), max_length=2
    )

class JoinRoomSerializer(serializers.Serializer):
    room_id = serializers.CharField(max_length=6)

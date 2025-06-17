# rooms/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source='host.username')
    players = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='username'
    )

    class Meta:
        model = Room
        fields = ('code', 'host', 'players', 'is_public', 'width', 'height', 'vs_ai', 'creator_color', 'created_at',
                  "closed_at", 'is_closed')

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('is_public', 'width', 'height', 'vs_ai', 'creator_color')

    def create(self, validated):
        user = self.context['request'].user
        room = Room.objects.create(host=user, **validated)
        room.players.add(user)
        return room

class JoinRoomSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        try:
            room = Room.objects.get(code=value)
        except Room.DoesNotExist:
            raise serializers.ValidationError("invalid room code")
        if room.is_closed:
            raise serializers.ValidationError("room is closed")
        if room.is_full:
            raise serializers.ValidationError("room is full")
        return room

    def save(self):
        room = self.validated_data['code']
        user = self.context['request'].user
        if room.players.filter(pk=user.pk).exists():
            raise serializers.ValidationError("already in room")
        room.players.add(user)

        if room.is_full:
            room.closed_at = timezone.now()
            room.save()

        return room

class LeaveRoomSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        try:
            return Room.objects.get(code=value)
        except Room.DoesNotExist:
            raise serializers.ValidationError("invalid room code")

    def save(self):
        room = self.validated_data['code']
        user = self.context['request'].user
        if not room.players.filter(pk=user.pk).exists():
            raise serializers.ValidationError("not in room")
        room.players.remove(user)

        if room.is_empty:
            room.delete()
        else:
            room.save()

        return room

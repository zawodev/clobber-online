# rooms/serializers.py
from rest_framework import serializers
from challenges.models import Challenge
from challenges.serializers import ChallengeSerializer
from django.utils import timezone
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source='host.username')
    players = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='username'
    )
    challenge = ChallengeSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ('code', 'host', 'players', 'is_public', 'width', 'height', 'vs_ai', 'creator_color', 'created_at',
                  "closed_at", 'is_closed', 'is_full', 'is_empty', 'challenge')

class CreateRoomSerializer(serializers.ModelSerializer):

    challenge_id = serializers.IntegerField(
        write_only=True, required=False
    )

    class Meta:
        model = Room
        fields = ('is_public', 'width', 'height', 'vs_ai', 'creator_color', 'challenge_id')

    def validate_challenge_id(self, value):
        if value is None:
            return None
        try:
            return Challenge.objects.get(pk=value)
        except Challenge.DoesNotExist:
            raise serializers.ValidationError("invalid challenge_id")

    def create(self, validated):
        user = self.context['request'].user
        challenge = validated.pop('challenge_id', None)
        # jeśli jest challenge, vs_ai=true i nadpisujemy dimensions i color
        if challenge:
            validated['vs_ai'] = True
            validated['width'] = challenge.width
            validated['height'] = challenge.height
            validated['creator_color'] = challenge.player_color
        room = Room.objects.create(host=user, **validated)
        room.players.add(user)
        # przypisz challenge
        if challenge:
            room.challenge = challenge
            room.save()
        return room

class JoinRoomSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, value):
        try:
            room = Room.objects.get(code=value)
        except Room.DoesNotExist:
            raise serializers.ValidationError("invalid room code")
        #if room.is_closed:
        #    raise serializers.ValidationError("room is closed")
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

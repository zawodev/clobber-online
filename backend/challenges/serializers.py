# challenges/serializers.py
from rest_framework import serializers
from .models import Challenge

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('id', 'title', 'description', 'width', 'height', 'board', 'player_color', 'created_at')

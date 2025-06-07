from rest_framework import serializers
from .models import GameResult

class GameResultSerializer(serializers.ModelSerializer):
    winner = serializers.CharField(source='winner.username')
    loser = serializers.CharField(source='loser.username')

    class Meta:
        model = GameResult
        fields = ('id', 'winner', 'loser', 'played_at')

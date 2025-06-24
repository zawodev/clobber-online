from rest_framework import serializers
from .models import GameResult

class GameResultSerializer(serializers.ModelSerializer):
    winner = serializers.SerializerMethodField()
    loser = serializers.SerializerMethodField()

    class Meta:
        model = GameResult
        fields = ('id', 'winner', 'loser', 'played_at')

    def get_winner(self, obj):
        return obj.winner.username if obj.winner else None

    def get_loser(self, obj):
        return obj.loser.username if obj.loser else None

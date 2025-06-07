from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import GameResultSerializer
from .models import GameResult
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination

class UserGameHistoryView(generics.ListAPIView):
    serializer_class = GameResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return GameResult.objects.filter(
            Q(winner=user) | Q(loser=user)
        ).order_by('-played_at')

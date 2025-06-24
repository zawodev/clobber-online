from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import GameResultSerializer
from .models import GameResult
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination

from django.contrib.auth import get_user_model

User = get_user_model()

class UserGameHistoryView(generics.ListAPIView):
    serializer_class = GameResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if not username:
            user = self.request.user
        else:
            user = generics.get_object_or_404(User, username=username)
        return GameResult.objects.filter(
            Q(winner=user) | Q(loser=user)
        ).order_by('-played_at')

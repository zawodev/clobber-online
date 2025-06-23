# challenges/views.py
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Challenge
from .serializers import ChallengeSerializer

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.order_by('-created_at')
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]  # lub ograniczyć adminami jeśli ich zrobimy

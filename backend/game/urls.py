# game/urls.py
from django.urls import path
from .views import UserGameHistoryView

urlpatterns = [
    path('history/', UserGameHistoryView.as_view(), name='user-game-history'),
]

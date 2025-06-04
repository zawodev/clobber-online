# rooms/urls.py
from django.urls import path
from .views import (
    CreateRoomView, PublicRoomsList,
    RoomDetailView, JoinRoomView, LeaveRoomView
)

urlpatterns = [
    path('create/', CreateRoomView.as_view()),
    path('public/', PublicRoomsList.as_view()),
    path('join/', JoinRoomView.as_view()),
    path('leave/', LeaveRoomView.as_view()),
    path('details/<str:code>/', RoomDetailView.as_view()),
]

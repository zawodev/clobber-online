# rooms/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count

from .models import Room
from .serializers import (
    RoomSerializer, CreateRoomSerializer,
    JoinRoomSerializer, LeaveRoomSerializer
)

class CreateRoomView(generics.GenericAPIView):
    serializer_class = CreateRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        room = ser.save()
        return Response(RoomSerializer(room).data)

class PublicRoomsList(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Room.objects.annotate(
            players_count=Count('players')
        ).filter(
            is_public=True,
            players_count__gte=1
        )

class RoomDetailView(generics.RetrieveAPIView):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'code'
    queryset = Room.objects.all()

class JoinRoomView(generics.GenericAPIView):
    serializer_class = JoinRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        room = ser.save()
        return Response(RoomSerializer(room).data)

class LeaveRoomView(generics.GenericAPIView):
    serializer_class = LeaveRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        room = ser.save()
        return Response({"detail": f"left room {room.code}"})

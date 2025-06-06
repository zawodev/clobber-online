# rooms/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response

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
    queryset = Room.objects.filter(is_public=True)

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

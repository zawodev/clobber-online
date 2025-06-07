# users/views.py
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework import generics, status, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.views import APIView

from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FriendRequest, User, EmailToken
from .serializers import FriendSerializer, RegisterSerializer, UserSerializer, FriendRequestSerializer, \
    IncomingFriendRequestSerializer, AvatarUploadSerializer

# import Token
from rest_framework.authtoken.models import Token



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"error": "username or email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ConfirmEmailView(generics.GenericAPIView):
    def get(self, request, token):
        try:
            et = EmailToken.objects.get(token=token)
            et.user.email_confirmed = True
            et.user.save()
            return Response({'status': 'email confirmed'})
        except EmailToken.DoesNotExist:
            return Response({'error': 'invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    def post(self, request):
        u = request.data.get('username')
        p = request.data.get('password')
        user = authenticate(username=u, password=p)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'bad credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AvatarUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AvatarUploadSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendAddView(generics.GenericAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        friend_name = request.data.get('friend_username')
        try:
            f = User.objects.get(username=friend_name)
            request.user.friends.add(f)
            return Response({'status': 'friend added'})
        except User.DoesNotExist:
            return Response({'error': 'no such user'}, status=status.HTTP_404_NOT_FOUND)


class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def perform_create(self, serializer):
        to_username = self.request.data.get('to_username')
        to_user = User.objects.get(username=to_username)
        serializer.save(from_user=self.request.user, to_user=to_user)


class IncomingFriendRequestsView(generics.ListAPIView):
    serializer_class = IncomingFriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)


class RespondFriendRequestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        action = request.data.get('action')  # "accept" lub "decline"
        try:
            fr = FriendRequest.objects.get(pk=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'no such request'}, status=404)

        if action == 'accept':
            request.user.friends.add(fr.from_user)
            fr.from_user.friends.add(request.user)
            fr.delete()
            return Response({'status': 'accepted'})
        elif action == 'decline':
            fr.delete()
            return Response({'status': 'declined'})
        else:
            return Response({'error': 'invalid action'}, status=400)

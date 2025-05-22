# users/views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserSerializer, FriendRequestSerializer
from .models import FriendRequest

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    Rejestracja użytkownika. Tworzy nowego użytkownika z is_active=False
    i wysyła e-mail aktywacyjny.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Generujemy token i uid dla linku aktywacyjnego
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"http://localhost:8000/api/activate/{uid}/{token}/"
        # Wysyłamy e-mail z linkiem (używamy send_mail z Django):contentReference[oaicite:9]{index=9}
        subject = 'Aktywuj swoje konto'
        message = f'Kliknij w link, aby aktywować konto: {activation_link}'
        send_mail(subject, message, 'from@example.com', [user.email], fail_silently=False)


class ActivateView(APIView):
    """
    Aktywacja konta użytkownika po kliknięciu w link z e-maila.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Konto aktywowane.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Niepoprawny link aktywacyjny.'},
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    """
    Wyświetlanie własnego profilu (zalogowany użytkownik).
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileDetailView(generics.RetrieveAPIView):
    """
    Wyświetlanie profilu innego użytkownika (po podaniu username w URL).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated]


class FriendRequestListView(generics.ListAPIView):
    """
    Lista przychodzących zaproszeń dla zalogowanego użytkownika.
    """
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)


class SendFriendRequestView(APIView):
    """
    Wysyłanie zaproszenia do znajomych (nadawca = current user).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            to_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'Użytkownik nie istnieje.'},
                            status=status.HTTP_404_NOT_FOUND)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'detail': 'Zaproszenie już wysłane.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if to_user == request.user:
            return Response({'detail': 'Nie możesz dodać siebie.'},
                            status=status.HTTP_400_BAD_REQUEST)
        fr = FriendRequest(from_user=request.user, to_user=to_user)
        fr.save()
        return Response({'detail': 'Zaproszenie wysłane.'}, status=status.HTTP_201_CREATED)


class FriendRequestAcceptView(APIView):
    """
    Akceptowanie zaproszenia do znajomych. Dodaje obu użytkowników do swoich list znajomych.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            fr = FriendRequest.objects.get(pk=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Zaproszenie nie istnieje.'},
                            status=status.HTTP_404_NOT_FOUND)
        # Dodaj obu użytkowników do swoich list znajomych (symetrycznie):contentReference[oaicite:10]{index=10}
        request.user.friends.add(fr.from_user)
        fr.from_user.friends.add(request.user)
        fr.delete()  # usuwamy zaakceptowane zaproszenie
        return Response({'detail': 'Zaproszenie zaakceptowane.'}, status=status.HTTP_200_OK)


class FriendRequestRejectView(APIView):
    """
    Odrzucanie zaproszenia (po prostu usunięcie wpisu).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            fr = FriendRequest.objects.get(pk=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Zaproszenie nie istnieje.'},
                            status=status.HTTP_404_NOT_FOUND)
        fr.delete()
        return Response({'detail': 'Zaproszenie odrzucone.'}, status=status.HTTP_200_OK)

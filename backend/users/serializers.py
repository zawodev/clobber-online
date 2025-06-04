# users/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import FriendRequest, User, EmailToken

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already taken")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already registered")
        return value

    def create(self, validated):
        user = User.objects.create_user(
            username=validated['username'],
            email=validated['email'],
            password=validated['password'])
        token = EmailToken.objects.create(user=user)
        # tu: wysyłka maila z token.token
        activation_link = f"http://localhost:8000/api/v1/users/confirm/{token.token}/"
        print(f"confirmation link: {activation_link}")
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'email_confirmed', 'avatar', 'elo', 'friends')


class FriendSerializer(serializers.Serializer):
    friend_username = serializers.CharField()


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.username')
    to_user = serializers.ReadOnlyField(source='to_user.username')

    def validate_to_username(self, value):
        try:
            to_user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        if to_user == self.context['request'].user:
            raise serializers.ValidationError("cannot friend yourself")
        # sprawdź czy już są znajomymi
        if to_user in self.context['request'].user.friends.all():
            raise serializers.ValidationError("already friends")
        # sprawdź czy request już istnieje
        if FriendRequest.objects.filter(
                from_user=self.context['request'].user,
                to_user=to_user
        ).exists():
            raise serializers.ValidationError("friend request already sent")
        return value

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'created')

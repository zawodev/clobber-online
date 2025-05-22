# users/serializers.py
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import FriendRequest

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        # Tworzymy użytkownika i ustawiamy is_active=False przed potwierdzeniem e-mail
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.is_active = False
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    friends = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'avatar', 'elo', 'friends')


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.username')
    to_user = serializers.ReadOnlyField(source='to_user.username')

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'created')

# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)                   # unikalny e-mail
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    elo = models.IntegerField(default=1000)
    friends = models.ManyToManyField('self', blank=True)     # lista znajomych (symetryczna relacja)

    USERNAME_FIELD = 'email'   # używamy e-maila do logowania
    REQUIRED_FIELDS = ['username']  # pola wymagane przy tworzeniu użytkownika

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # unikamy duplikatów zaproszeń

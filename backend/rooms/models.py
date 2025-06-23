import random
import string
from django.db import models
from django.conf import settings

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Room(models.Model):
    code = models.CharField(max_length=6, unique=True, default=generate_code)
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hosted_rooms'
    )
    players = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='rooms'
    )
    creator_color = models.CharField(
        max_length=5,
        choices=[('black', 'black'), ('white', 'white')],
        default='black'
    )
    challenge = models.ForeignKey(
        'challenges.Challenge',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    vs_ai = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    width = models.PositiveIntegerField(default=8)
    height = models.PositiveIntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_empty(self):
        return self.players.count() == 0

    @property
    def is_full(self):
        if self.vs_ai:
            return self.players.count() >= 1
        return self.players.count() >= 2

    @property
    def is_closed(self):
        return self.closed_at is not None

    def __str__(self):
        return f"{self.code} ({'public' if self.is_public else 'private'})"

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField  # lub models.JSONField

STATUS_CHOICES = [
    ('waiting', 'waiting'),
    ('playing', 'playing'),
    ('finished', 'finished'),
]

class Game(models.Model):
    room = models.OneToOneField('rooms.Room', on_delete=models.CASCADE)
    board = models.JSONField(default=list)   # np. [[0]*width]*height
    current = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='+')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    created = models.DateTimeField(auto_now_add=True)

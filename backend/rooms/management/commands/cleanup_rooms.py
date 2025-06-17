# rooms/management/commands/cleanup_rooms.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from rooms.models import Room
from datetime import timedelta
from django.db.models import Count

class Command(BaseCommand):
    help = "usuń pokoje starze niż 1h"

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=0) # for debug i set this to 0, later change to any number
        stale = Room.objects.filter(created_at__lt=cutoff)
        count = stale.count()
        stale.delete()
        self.stdout.write(f"deleted {count} rooms older than 1h")

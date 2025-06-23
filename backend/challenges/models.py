from django.db import models

class Challenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    # JSONField: list of lists with 'b','w','_' values
    board = models.JSONField()
    player_color = models.CharField(
        max_length=5,
        choices=[('black', 'black'), ('white', 'white')]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

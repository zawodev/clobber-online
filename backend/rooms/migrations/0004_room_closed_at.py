# Generated by Django 5.2.1 on 2025-06-16 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_room_creator_color_room_vs_ai'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

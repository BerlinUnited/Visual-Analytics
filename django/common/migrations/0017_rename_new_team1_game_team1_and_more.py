# Generated by Django 5.1.2 on 2025-06-25 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0016_remove_game_team1_remove_game_team2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='new_team1',
            new_name='team1',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='new_team2',
            new_name='team2',
        ),
    ]

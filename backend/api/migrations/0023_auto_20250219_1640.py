# Generated by Django 5.1.2 on 2025-02-19 16:40

from django.db import migrations


def migrate_logs_away_from_gfk(apps, schema_editor):
    Log = apps.get_model('api', 'Log')
    Game = apps.get_model('api', 'Game')
    Experiment = apps.get_model('api', 'Experiment')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Get the ContentType for the Game model
    game_content_type = ContentType.objects.get_for_model(Game)
    experiment_content_type = ContentType.objects.get_for_model(Experiment)

    # Iterate over Log objects with the Game content type
    for log in Log.objects.filter(content_type=game_content_type):
        # Get the corresponding Game object
        game = Game.objects.get(id=log.object_id)
        # Update the log's log_game fk field
        log.log_game = game
        log.save()
    
    for log in Log.objects.filter(content_type=experiment_content_type):
        # Get the corresponding Game object
        experiment = Experiment.objects.get(id=log.object_id)
        # Update the log's log_experiment fk field
        log.log_experiment = experiment
        log.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_log_log_experiment_log_log_game'),
    ]

    operations = [
        migrations.RunPython(migrate_logs_away_from_gfk),
    ]

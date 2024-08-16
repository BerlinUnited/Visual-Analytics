# Generated by Django 5.0.6 on 2024-08-16 11:49

import django.contrib.postgres.fields.ranges
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('time', django.contrib.postgres.fields.ranges.DateTimeRangeField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FrameTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_number', models.IntegerField(blank=True, null=True)),
                ('frame_time', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera', models.CharField(blank=True, choices=[('TOP', 'Top'), ('BOTTOM', 'Bottom')], max_length=10, null=True)),
                ('type', models.CharField(blank=True, choices=[('RAW', 'raw'), ('JPEG', 'jpeg')], max_length=10, null=True)),
                ('frame_number', models.IntegerField(blank=True, null=True)),
                ('image_url', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.CharField(blank=True, max_length=100, null=True)),
                ('team2', models.CharField(blank=True, max_length=100, null=True)),
                ('half', models.CharField(blank=True, max_length=100, null=True)),
                ('is_testgame', models.BooleanField(blank=True, null=True)),
                ('head_ref', models.CharField(blank=True, max_length=100, null=True)),
                ('assistent_ref', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('field', models.CharField(blank=True, max_length=100, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='api.event')),
            ],
            options={
                'unique_together': {('event', 'start_time', 'half')},
            },
        ),
        migrations.CreateModel(
            name='ImageAnnotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ImageAnnotation', to='api.image')),
            ],
        ),
        migrations.CreateModel(
            name='RobotData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('robot_version', models.CharField(blank=True, max_length=5, null=True)),
                ('player_number', models.IntegerField(blank=True, null=True)),
                ('head_number', models.IntegerField(blank=True, null=True)),
                ('body_serial', models.CharField(blank=True, max_length=20, null=True)),
                ('head_serial', models.CharField(blank=True, max_length=20, null=True)),
                ('representations', models.JSONField(blank=True, null=True)),
                ('sensor_log_path', models.CharField(blank=True, max_length=200, null=True)),
                ('log_path', models.CharField(blank=True, max_length=200, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='robot_data', to='api.game')),
            ],
            options={
                'unique_together': {('game', 'player_number', 'head_number')},
            },
        ),
        migrations.AddField(
            model_name='image',
            name='log',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.robotdata'),
        ),
        migrations.CreateModel(
            name='SensorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_frame_number', models.IntegerField(blank=True, null=True)),
                ('sensor_frame_time', models.IntegerField(blank=True, null=True)),
                ('representation_name', models.CharField(blank=True, max_length=40, null=True)),
                ('representation_data', models.JSONField(blank=True, null=True)),
                ('robotdata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensorlogs', to='api.robotdata')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together={('log', 'camera', 'type', 'frame_number')},
        ),
    ]

# Generated by Django 5.0.6 on 2024-08-08 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_frame_number_sensorlog_sensor_frame_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensorlog',
            name='log',
        ),
    ]

# Generated by Django 5.1.2 on 2025-06-23 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motion', '0004_alter_motionframe_closest_cognition_frame'),
    ]

    operations = [
        migrations.AddField(
            model_name='accelerometerdata',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='accelerometerdata',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='buttondata',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='buttondata',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fsrdata',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fsrdata',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gyrometerdata',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gyrometerdata',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='imudata',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='imudata',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inertialsensordata',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inertialsensordata',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='motionstatus',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='motionstatus',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='motorjointdata',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='motorjointdata',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorjointdata',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorjointdata',
            name='start_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.1.2 on 2025-02-15 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_videorecording_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CognitionFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_number', models.IntegerField(blank=True, null=True)),
                ('log_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cognitionframe', to='api.log')),
            ],
        ),
        migrations.CreateModel(
            name='MotionFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_number', models.IntegerField(blank=True, null=True)),
                ('log_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motionframe', to='api.log')),
            ],
        ),
    ]

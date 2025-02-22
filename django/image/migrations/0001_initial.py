# Generated by Django 5.1.2 on 2025-02-22 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NaoImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera', models.CharField(blank=True, choices=[('TOP', 'Top'), ('BOTTOM', 'Bottom')], max_length=10, null=True)),
                ('type', models.CharField(blank=True, choices=[('RAW', 'raw'), ('JPEG', 'jpeg')], max_length=10, null=True)),
                ('frame_number', models.IntegerField(blank=True, null=True)),
                ('image_url', models.CharField(blank=True, max_length=200, null=True)),
                ('blurredness_value', models.IntegerField(blank=True, null=True)),
                ('brightness_value', models.IntegerField(blank=True, null=True)),
                ('resolution', models.CharField(blank=True, max_length=11, null=True)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='common.log')),
            ],
            options={
                'unique_together': {('log', 'camera', 'type', 'frame_number')},
            },
        ),
    ]

# Generated by Django 5.1.2 on 2025-06-24 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_remove_videorecording_urls_event_event_folder_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]

# Generated by Django 5.1.2 on 2025-04-02 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_logstatus_teammessagedecision'),
    ]

    operations = [
        migrations.AddField(
            model_name='logstatus',
            name='BehaviorStateSparse',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

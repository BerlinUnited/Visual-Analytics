# Generated by Django 5.1.2 on 2025-04-02 09:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0007_logstatus_teamstate"),
    ]

    operations = [
        migrations.AddField(
            model_name="logstatus",
            name="AudioData",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

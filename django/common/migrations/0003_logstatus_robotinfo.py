# Generated by Django 5.1.2 on 2025-04-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0002_rename_num_bottom_logstatus_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="logstatus",
            name="RobotInfo",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

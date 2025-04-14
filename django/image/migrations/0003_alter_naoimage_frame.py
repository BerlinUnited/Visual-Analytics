# Generated by Django 5.1.2 on 2025-02-26 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cognition", "0002_initial"),
        ("image", "0002_alter_naoimage_unique_together_naoimage_frame_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="naoimage",
            name="frame",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="cognition.cognitionframe",
            ),
        ),
    ]

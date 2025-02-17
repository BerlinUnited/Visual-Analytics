# Generated by Django 5.1.2 on 2025-02-20 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_cognitionframe_frame_time_motionframe_frame_time'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cognitionframe',
            unique_together={('log_id', 'frame_number')},
        ),
        migrations.AlterUniqueTogether(
            name='motionframe',
            unique_together={('log_id', 'frame_number')},
        ),
        migrations.AddIndex(
            model_name='cognitionframe',
            index=models.Index(fields=['log_id', 'frame_number'], name='api_cogniti_log_id__145721_idx'),
        ),
        migrations.AddIndex(
            model_name='motionframe',
            index=models.Index(fields=['log_id', 'frame_number'], name='api_motionf_log_id__59a223_idx'),
        ),
    ]

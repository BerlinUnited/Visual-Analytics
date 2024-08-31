# Generated by Django 5.0.6 on 2024-08-31 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_type_imageannotation_annotation_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotation_id', models.CharField(max_length=100)),
                ('annotation', models.JSONField(blank=True, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Annotation', to='api.image')),
            ],
        ),
        migrations.DeleteModel(
            name='ImageAnnotation',
        ),
    ]

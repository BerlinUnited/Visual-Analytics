# Generated by Django 5.0.6 on 2024-08-16 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_vatuser_name_alter_vatuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vatuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='vatuser',
            name='last_name',
        ),
    ]

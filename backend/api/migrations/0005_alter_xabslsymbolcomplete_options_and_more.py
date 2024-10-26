# Generated by Django 5.1.2 on 2024-10-26 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_xabslsymbolcomplete_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='xabslsymbolcomplete',
            options={'verbose_name_plural': 'XabslSymbolComplete'},
        ),
        migrations.AlterModelOptions(
            name='xabslsymbolsparse',
            options={'verbose_name_plural': 'XabslSymbolSparse'},
        ),
        migrations.RemoveField(
            model_name='logstatus',
            name='id',
        ),
        migrations.AlterField(
            model_name='logstatus',
            name='log_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='log_status', serialize=False, to='api.log'),
        ),
        migrations.AlterField(
            model_name='xabslsymbolcomplete',
            name='log_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='xabsl_symbol_complete', serialize=False, to='api.log'),
        ),
    ]

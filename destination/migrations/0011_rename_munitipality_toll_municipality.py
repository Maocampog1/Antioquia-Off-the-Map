# Generated by Django 5.1.6 on 2025-03-19 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0010_toll'),
    ]

    operations = [
        migrations.RenameField(
            model_name='toll',
            old_name='munitipality',
            new_name='municipality',
        ),
    ]

# Generated by Django 5.1.6 on 2025-03-08 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0005_category_remove_municipality_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('price_range', models.CharField(max_length=255)),
                ('cuisine_type', models.CharField(max_length=255)),
                ('contact_info', models.CharField(max_length=255)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='destination.municipality')),
            ],
        ),
    ]

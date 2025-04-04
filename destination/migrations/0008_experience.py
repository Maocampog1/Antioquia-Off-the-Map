# Generated by Django 5.1.6 on 2025-03-08 20:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('destination', '0007_activity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('donde_comer', 'Dónde comer'), ('donde_dormir', 'Dónde dormir'), ('que_hacer', 'Qué hacer')], max_length=50)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='destination.municipality')),
            ],
        ),
    ]

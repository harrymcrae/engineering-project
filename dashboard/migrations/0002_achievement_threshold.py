# Generated by Django 5.1.6 on 2025-03-24 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='threshold',
            field=models.IntegerField(default=0),
        ),
    ]

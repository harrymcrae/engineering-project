# Generated by Django 5.1.6 on 2025-03-24 10:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0005_remove_badge_points_awarded'),
        ('dashboard', '0003_achievement_achievement_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='badge_awarded',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='badges.badge'),
        ),
    ]

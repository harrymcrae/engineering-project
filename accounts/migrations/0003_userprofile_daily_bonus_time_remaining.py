# Generated by Django 5.1.6 on 2025-02-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_registration_bonus_claimed_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='daily_bonus_time_remaining',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

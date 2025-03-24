# Generated by Django 5.1.6 on 2025-03-23 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='achievements',
            field=models.ManyToManyField(blank=True, related_name='user_profiles', to='dashboard.achievement'),
        ),
    ]

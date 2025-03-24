from django.db import models
from django.contrib.auth.models import User
from badges.models import Badge

class Achievement(models.Model):
    achievement_name = models.CharField(max_length=50,null=True)
    achievement_description = models.CharField(max_length=255,null=True)
    achievement_id = models.CharField(max_length=10, null=True)
    points_awarded = models.IntegerField(default=0)
    threshold = models.IntegerField(default=0)
    achievement_type = models.CharField(max_length=30, null=True)
    badge_awarded = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.achievement_name} Achievement"

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from challenges.models import Quiz, Challenge

class UserProfile(models.Model):
    PLAYER = 'player'
    GAME_KEEPER = 'game_keeper'
    DEVELOPER = 'developer'

    USER_TYPE_CHOICES = [
        (PLAYER, 'Player'),
        (GAME_KEEPER, 'Game Keeper'),
        (DEVELOPER, 'Developer'),
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=PLAYER)
    points = models.IntegerField(default=0)
    registration_bonus_claimed = models.BooleanField(default=False)
    daily_bonus_time_claimed = models.DateTimeField(null=True,blank=True)
    challenges_completed = models.ManyToManyField(Challenge, blank=True)
    quizzes_completed = models.ManyToManyField(Quiz, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


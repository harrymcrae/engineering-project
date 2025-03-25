from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from challenges.models import Quiz, Challenge
from badges.models import Badge
from dashboard.models import Achievement

class UserProfile(models.Model):
    PLAYER = 'player'
    GAME_KEEPER = 'game_keeper'
    DEVELOPER = 'developer'

    USER_TYPE_CHOICES = [
        (PLAYER, 'Player'),
        (GAME_KEEPER, 'Game Keeper'),
        (DEVELOPER, 'Developer'),
    ]

    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=PLAYER)
    points = models.IntegerField(default=0)
    registration_bonus_claimed = models.BooleanField(default=False)
    daily_bonus_time_claimed = models.DateTimeField(null=True,blank=True)
    challenges_completed = models.ManyToManyField(Challenge, blank=True)
    quizzes_completed = models.ManyToManyField(Quiz, blank=True)
    badges = models.ManyToManyField(Badge, blank=True)
    completed_achievements = models.ManyToManyField(Achievement, blank=True, related_name='user_profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User) # Signal to create a user profile when a new user is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User) # Signal to save the user profile when the user is saved
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


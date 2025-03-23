from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Challenge(models.Model):
    challenge_name = models.CharField(max_length=50,null=True)
    challenge_description = models.CharField(max_length=255,null=True)
    challenge_id = models.CharField(max_length=30, null=True)
    points_awarded = models.IntegerField(default=0)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)


    def __str__(self):
        return f"{self.challenge_name} Challenge"

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='submissions/')
    approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.challenge_name}"
    
@receiver(post_save, sender=Submission)
def add_to_completed_challenges(sender, instance, **kwargs):
    if instance.approved:
        instance.user.profile.challenges_completed.add(instance.challenge)

class Bonus(models.Model):
    bonus_name = models.CharField(max_length=50,null=True)
    bonus_description = models.CharField(max_length=255,null=True)
    bonus_id = models.CharField(max_length=30, null=True)
    points_awarded = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bonus_name}"

    class Meta:
        verbose_name = "Bonus"
        verbose_name_plural = "Bonuses"


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=50,null=True)
    quiz_description = models.CharField(max_length=255,null=True)
    quiz_id = models.CharField(max_length=50,null=True)
    quiz_question = models.CharField(max_length=255,null=True)
    quiz_option_one = models.CharField(max_length=255,null=True)
    quiz_option_two = models.CharField(max_length=255,null=True)
    quiz_option_three = models.CharField(max_length=255,null=True)
    quiz_option_four = models.CharField(max_length=255,null=True)
    quiz_answer = models.CharField(max_length=255,null=True)
    points_awarded = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quiz_name}"

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

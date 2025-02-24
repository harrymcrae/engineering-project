from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
    challenge_name = models.CharField(max_length=50,null=True)
    challenge_description = models.CharField(max_length=255,null=True)
    challenge_id = models.CharField(max_length=30, null=True)
    points_awarded = models.IntegerField(default=0)
    #image = models.URLField(blank=True, null=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)


    def __str__(self):
        return f"{self.challenge_name} Challenge"

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"

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

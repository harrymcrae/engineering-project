from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points') 
    filter_horizontal = ('quizzes_completed', 'challenges_completed', 'badges')
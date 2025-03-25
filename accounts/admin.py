from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile) # Register the UserProfile model with the admin panel
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'points') # Display these fields in the admin panel
    filter_horizontal = ('quizzes_completed', 'challenges_completed', 'badges', 'completed_achievements') # Allow for easier filtering of these fields
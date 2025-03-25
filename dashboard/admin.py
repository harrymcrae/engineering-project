from django.contrib import admin
from .models import Achievement
    
class AchievementAdmin(admin.ModelAdmin): # Customise the admin interface for achievements
    list_display = ('achievement_name', 'points_awarded')
    search_fields = ('achievement_name', 'achievement_description')  # Allow searching by name or description
    fields = ('achievement_name', 'achievement_id', 'achievement_description', 'points_awarded', 'threshold', 'achievement_type', 'badge_awarded')  # Fields visible in the admin form

admin.site.register(Achievement, AchievementAdmin)
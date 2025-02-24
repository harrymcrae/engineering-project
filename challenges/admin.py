from django.contrib import admin
from .models import Challenge, Quiz, Bonus


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('challenge_name', 'latitude', 'longitude')  # Display coordinates in the list
    search_fields = ('challenge_name', 'challenge_description')  # Allow searching by name or description
    fields = ('challenge_name', 'challenge_description', 'latitude', 'longitude','points_awarded')  # Fields visible in the admin form

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Quiz)
admin.site.register(Bonus)

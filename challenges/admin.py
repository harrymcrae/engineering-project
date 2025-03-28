from django.contrib import admin
from .models import Challenge, Quiz, Bonus, Submission


class ChallengeAdmin(admin.ModelAdmin): # Customise the admin interface for the Challenge model
    list_display = ('challenge_name', 'latitude', 'longitude')  # Display coordinates in the list
    search_fields = ('challenge_name', 'challenge_description')  # Allow searching by name or description
    fields = ('challenge_name', 'challenge_id', 'challenge_description', 'latitude', 'longitude','points_awarded')  # Fields visible in the admin form

class SubmissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(approved=False)  # only shows unapproved submissions

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Quiz)
admin.site.register(Bonus)
admin.site.register(Submission, SubmissionAdmin)

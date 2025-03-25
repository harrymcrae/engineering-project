from django.shortcuts import render
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required # This decorator ensures that only authenticated users can access this view
def leaderboard_page(request): # This view function retrieves all user profiles from the database, orders them by points in descending order, and assigns a rank to each user profile
    user_profiles = UserProfile.objects.select_related('user').order_by('-points')
    for i, profile in enumerate(user_profiles, start=1): # Enumerate is a built-in Python function that assigns a rank to each user profile
        profile.rank = i
    context = { # This dictionary contains the user profiles and passes them to the leaderboard.html template
        'user_profiles': user_profiles
    }
    return render(request, 'leaderboard.html', context)

from django.shortcuts import render
from accounts.models import UserProfile

def leaderboard_page(request):
    user_profiles = UserProfile.objects.select_related('user').order_by('-points')
    for i, profile in enumerate(user_profiles, start=1):
        profile.rank = i
    context = {
        'user_profiles': user_profiles
    }
    return render(request, 'leaderboard.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Achievement
from django.http import JsonResponse
import json

@login_required # Decorator to ensure that the user is logged in before accessing the dashboard page
def dashboard_page(request): # Function to render the dashboard page with the user's profile, achievements, challenges, quizzes, badges, and statistics
    user_profile = request.user.profile

    achievements = Achievement.objects.all()
    challenges = user_profile.challenges_completed.all() # Queryset of challenges completed by the user
    quizzes = user_profile.quizzes_completed.all()
    badges = user_profile.badges.all()

    completed_achievements = list(user_profile.completed_achievements.values_list('achievement_id', flat=True)) # List of completed achievements by the user
    completed_achievements_json = json.dumps(completed_achievements)

    total_completed_challenges = user_profile.challenges_completed.count()
    total_completed_quizzes = user_profile.quizzes_completed.count()
    total_claimed_badges = user_profile.badges.count()
    total_points = user_profile.points

    context = {
        'challenges': challenges,
        'quizzes': quizzes,
        'profile': user_profile,
        'badges': badges,
        'achievements': achievements,
        'completed_achievements': completed_achievements,
        'completed_achievements_json': completed_achievements_json,
        'total_completed_challenges': total_completed_challenges,
        'total_completed_quizzes': total_completed_quizzes,
        'total_points': total_points,
        'total_claimed_badges': total_claimed_badges
    }

    return render(request, 'dashboard.html', context)

def profile_view(request): # Function to render the user's profile page with their username
    return render(request, 'dashboard.html', {'username': request.user.username})

def check_achievement_completed(request, achievement_id): # Function to check if the achievement has been completed by the user
    profile = request.user.profile
    completed_achievements = achievement_id in profile.completed_achievements.values_list('achievement_id', flat=True) # Check if the achievement_id is in the list of completed achievements

    return JsonResponse({"completed_achievements": completed_achievements})


def achievement_reward(request, achievement_id): # Function to reward the user with points and badges upon completing an achievement
    if request.method == "POST": # Check if the request method is POST
        profile = request.user.profile
        achievement = Achievement.objects.get(achievement_id=achievement_id)
        badge = achievement.badge_awarded

        if achievement in profile.completed_achievements.all(): # Check if the user has already completed the achievement
            return JsonResponse({"success": False, "message": "You have already completed this achievement!"})
        
        profile.points += achievement.points_awarded # Add the points awarded for the achievement to the user's total points
        profile.completed_achievements.add(achievement)
        profile.badges.add(badge)
        profile.save()

        return JsonResponse({"success": True, "message": "Achievement completed! 🎉"})
    
    return JsonResponse({"success": False, "message": "Invalid request"})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Achievement
from django.http import JsonResponse
import json

@login_required
def dashboard_page(request):
    user_profile = request.user.profile

    achievements = Achievement.objects.all()
    challenges = user_profile.challenges_completed.all()
    quizzes = user_profile.quizzes_completed.all()
    badges = user_profile.badges.all()

    completed_achievements = list(user_profile.completed_achievements.values_list('achievement_id', flat=True))
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

def profile_view(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

def check_achievement_completed(request, achievement_id):
    profile = request.user.profile
    completed_achievements = achievement_id in profile.completed_achievements.values_list('achievement_id', flat=True)

    return JsonResponse({"completed_achievements": completed_achievements})


def achievement_reward(request, achievement_id):
    if request.method == "POST":
        profile = request.user.profile
        achievement = Achievement.objects.get(achievement_id=achievement_id)

        if achievement in profile.completed_achievements.all():
            return JsonResponse({"success": False, "message": "You have already completed this achievement!"})
        
        profile.points += achievement.points_awarded
        profile.completed_achievements.add(achievement)
        profile.save()

        return JsonResponse({"success": True, "message": "Achievement completed! 🎉"})
    
    return JsonResponse({"success": False, "message": "Invalid request"})

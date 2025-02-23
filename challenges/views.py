from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Challenge, Quiz
from accounts.models import UserProfile
import json

@login_required
def challenges_page(request):
    challenges = Challenge.objects.all()
    quizzes = Quiz.objects.all()

    user_profile = request.user.profile
    if user_profile.daily_bonus_time_claimed:
        time_remaining = 86400000 - int(((timezone.now() - user_profile.daily_bonus_time_claimed).total_seconds())*1000)
    else:
        user_profile.daily_bonus_time_claimed = 0

    quizzes_completed = list(user_profile.quizzes_completed.values_list('quiz_id', flat=True))
    quizzes_completed_json = json.dumps(quizzes_completed)

    context = {
        'challenges': challenges,
        'time_remaining': time_remaining,
        'quizzes': quizzes,
        'quizzes_completed': quizzes_completed_json,
    }
    return render(request, 'challenges.html', context)


def claim_daily_bonus(request):
    if request.method == "POST":
        profile = request.user.profile

        if profile.daily_bonus_time_claimed:
            time_remaining = 86400000 - int(((timezone.now() - profile.daily_bonus_time_claimed).total_seconds())*1000)
            if time_remaining > 0:
                return JsonResponse({'success': False,'message': 'You have already claimed the daily bonus!','time_remaining': time_remaining
                })


        profile.points += Challenge.objects.get(challenge_id='daily-bonus').points_awarded
        profile.daily_bonus_time_claimed = timezone.now()
        profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Daily bonus claimed! 🎉',
            'daily_bonus_time_claimed': int(profile.daily_bonus_time_claimed.timestamp() * 1000)  # Return time in milliseconds
        })

    return JsonResponse({"success": False, "message": "Invalid request."})

# Method to claim registration bonus
def claim_registration_bonus(request):
    if request.method == "POST":
        profile = request.user.profile

        if profile.registration_bonus_claimed:
            return JsonResponse({"success": False, "message": "You have already claimed the registration bonus!"})

        profile.points += Challenge.objects.get(challenge_id='registration-bonus').points_awarded
        profile.registration_bonus_claimed = True
        profile.save()

        return JsonResponse({"success": True, "message": "Registration bonus claimed! 🎉"})
    
    return JsonResponse({"success": False, "message": "Invalid request."})


# Method to check if registration bonus has been claimed
def check_registration_bonus_claimed(request):
    profile = request.user.profile  
    bonus_claimed = profile.registration_bonus_claimed

    return JsonResponse({"registration_bonus_claimed": bonus_claimed})

def quiz_reward(request, quiz_id):
    if request.method == "POST":
        profile = request.user.profile
        quiz = Quiz.objects.get(quiz_id=quiz_id)

        if quiz in profile.quizzes_completed.all():
            return JsonResponse({"success": False, "message": "You have already completed this quiz!"})
        
        profile.points += quiz.points_awarded
        profile.quizzes_completed.add(quiz)
        profile.save()

        return JsonResponse({"success": True, "message": "Quiz completed! 🎉"})
    
    return JsonResponse({"success": False, "message": "Invalid request"})

def check_quiz_completed(request, quiz_id):
    profile = request.user.profile
    quiz_completed = quiz_id in profile.quizzes_completed.values_list('quiz_id', flat=True)

    return JsonResponse({"quiz_completed": quiz_completed})




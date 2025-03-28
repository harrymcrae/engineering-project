from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Challenge, Quiz, Bonus, Submission
from accounts.models import UserProfile
from badges.models import Badge
import json
from .forms import SubmissionForm

@login_required
def challenges_page(request): # Render Challenges page, with all challenges, quizzes, bonuses, and
    challenges = Challenge.objects.all()
    quizzes = Quiz.objects.all()
    bonuses = Bonus.objects.all()

    user_profile = request.user.profile
    time_remaining = 0

    if user_profile.daily_bonus_time_claimed: # Calculate time remaining for daily bonus
        time_remaining = 86400000 - int(((timezone.now() - user_profile.daily_bonus_time_claimed).total_seconds())*1000)
    else:
        user_profile.daily_bonus_time_claimed = 0

    quizzes_completed = list(user_profile.quizzes_completed.values_list('quiz_id', flat=True))
    quizzes_completed_json = json.dumps(quizzes_completed)

    challenges_completed = list(user_profile.challenges_completed.values_list('challenge_id', flat=True))
    challenges_completed_json = json.dumps(challenges_completed)

    pending = Submission.objects.filter(user=request.user, approved=False)

    pending_submissions = [submission.challenge.challenge_id for submission in pending]
    pending_submissions_json = json.dumps(pending_submissions)

    context = {
        'challenges': challenges,
        'time_remaining': time_remaining,
        'quizzes': quizzes,
        'bonuses': bonuses,
        'quizzes_completed': quizzes_completed,
        'challenges_completed': challenges_completed,
        'quizzes_completed_json': quizzes_completed_json,
        'challenges_completed_json': challenges_completed_json,
        'pending_submissions': pending_submissions,
        'pending_submissions_json': pending_submissions_json,
    }
    return render(request, 'challenges.html', context)


def claim_daily_bonus(request): # Method to claim daily bonus
    if request.method == "POST":
        profile = request.user.profile

        if profile.daily_bonus_time_claimed: # Check if daily bonus has already been claimed
            time_remaining = 86400000 - int(((timezone.now() - profile.daily_bonus_time_claimed).total_seconds())*1000)
            if time_remaining > 0:
                return JsonResponse({'success': False,'message': 'You have already claimed the daily bonus!','time_remaining': time_remaining})


        profile.points += Bonus.objects.get(bonus_id='daily-bonus').points_awarded # Add points to user profile
        profile.daily_bonus_time_claimed = timezone.now()
        profile.save()

        return JsonResponse({ # Return success message
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

        profile.points += Bonus.objects.get(bonus_id='registration-bonus').points_awarded
        profile.registration_bonus_claimed = True
        profile.save()

        return JsonResponse({"success": True, "message": "Registration bonus claimed! 🎉"})
    
    return JsonResponse({"success": False, "message": "Invalid request."})


# Method to check if registration bonus has been claimed
def check_registration_bonus_claimed(request):
    profile = request.user.profile  
    bonus_claimed = profile.registration_bonus_claimed

    return JsonResponse({"registration_bonus_claimed": bonus_claimed})

def quiz_reward(request, quiz_id): # Method to reward user for completing quiz
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

def check_quiz_completed(request, quiz_id): # Method to check if quiz has been completed
    profile = request.user.profile
    quiz_completed = quiz_id in profile.quizzes_completed.values_list('quiz_id', flat=True)

    return JsonResponse({"quiz_completed": quiz_completed})

def challenge_reward(request, challenge_id): # Method to reward user for completing challenge
    if request.method == "POST":
        profile = request.user.profile
        challenge = Challenge.objects.get(challenge_id=challenge_id) # Get challenge object

        if challenge in profile.challenges_completed.all():
            return JsonResponse({"success": False, "message": "You have already completed this challenge!"})

        profile.points += challenge.points_awarded
        profile.challenges_completed.add(challenge)
        profile.save()

        return JsonResponse({"success": True, "message": "Challenge completed! 🎉"})
    
    return JsonResponse({"success": False, "message": "Invalid request"})

def check_challenge_completed(request, challenge_id): # Method to check if challenge has been completed
    profile = request.user.profile
    challenge_completed = challenge_id in profile.challenges_completed.values_list('challenge_id', flat=True)

    return JsonResponse({"challenge_completed": challenge_completed})

def submit_proof(request, challenge_id): # Method to submit proof for challenge
    challenge = Challenge.objects.get(challenge_id=challenge_id)
    user = request.user

    existing_submission = Submission.objects.filter(user=user, challenge=challenge, approved=False).first()
    if existing_submission: # Check if user already has an unapproved submission
        return JsonResponse({'success': False, 'error': 'You already have an unapproved submission for this challenge.'})

    if request.method == "POST" and request.FILES.get("image"): # Check if request is POST and image is uploaded

        submission = Submission.objects.create( # Create submission object
            user=request.user,
            challenge=challenge,
            image=request.FILES["image"],
            approved=False,
        )

        return JsonResponse({"success": True, "message": "Submission received!"})

    return JsonResponse({"success": False, "error": "Invalid request"})

def check_has_submission(request, challenge_id): # Method to check if user has already submitted proof for challenge
    challenge = Challenge.objects.get(challenge_id=challenge_id)
    submission = Submission.objects.filter(user=request.user, challenge=challenge).first()

    if not submission:
        return JsonResponse({"has_submission": False, "approved": False})

    return JsonResponse({"has_submission": True, "approved":submission.approved})

def submission_reward(request, challenge_id):
    if request.method == "POST":
        profile = request.user.profile
        challenge = Challenge.objects.get(challenge_id=challenge_id)

        submission = Submission.objects.filter(user=request.user, challenge=challenge, approved=True).first()

        if not submission:
            return JsonResponse({"success": False, "message": "No approved submission found!"})

        if challenge in profile.challenges_completed.all():
            return JsonResponse({"success": False, "message": "You have already completed this challenge!"})

        profile.points += challenge.points_awarded
        profile.challenges_completed.add(challenge)
        profile.save()

        submission.delete()

        return JsonResponse({"success": True, "message": "Challenge completed! 🎉"})

    return JsonResponse({"success": False, "message": "Invalid request"})
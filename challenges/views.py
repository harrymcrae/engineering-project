from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse

@login_required
def challenges_page(request):
    return render(request, 'challenges.html')

# Method to claim registration bonus
def claim_registration_bonus(request):
    if request.method == "POST":
        profile = request.user.profile

        if profile.registration_bonus_claimed:
            return JsonResponse({"success": False, "message": "You have already claimed the registration bonus!"})

        profile.points += 10
        profile.registration_bonus_claimed = True
        profile.save()

        return JsonResponse({"success": True, "message": "Registration bonus claimed! 🎉"})
    
    return JsonResponse({"success": False, "message": "Invalid request."})

# Method to check if registration bonus has been claimed
def check_registration_bonus_claimed(request):
    profile = request.user.profile  
    bonus_claimed = profile.registration_bonus_claimed

    return JsonResponse({"registration_bonus_claimed": bonus_claimed})
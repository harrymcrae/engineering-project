from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from badges.models import Badge
from accounts.models import UserProfile
from django.http import JsonResponse

@login_required
def shop_page(request): # This view will display all the badges that are purchasable and not owned by the user``
    user_profile = request.user.profile

    badges = Badge.objects.filter(purchasable=True).exclude(id__in=user_profile.badges.values('id')).order_by('price')
    user_points = user_profile.points

    context = {
        'badges': badges,
        'user_points': user_points
    }

    return render(request, 'shop.html', context)

def purchase_badge(request, name): # This view will handle the purchase of a badge
    if request.method == "POST": # Check if the request is a POST request
        profile = request.user.profile
        badge = Badge.objects.get(name=name) # Get the badge object by name

        if badge in profile.badges.all(): # Check if the user already owns the badge
            return JsonResponse({"success": False, "message": "You already own this badge!"})

        if badge.purchasable and profile.points >= badge.price: # Check if the badge is purchasable and the user has enough points
            profile.badges.add(badge)
            profile.points -= badge.price
            profile.save()

            return JsonResponse({"success": True, "message": "Badge purchased! 🎉", "user_points": profile.points})
        else:
            return JsonResponse({"success": False, "message": "You do not have enough points to purchase this badge!"})
    
    return JsonResponse({"success": False, "message": "Invalid request"})


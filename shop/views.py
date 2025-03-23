from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from badges.models import Badge
from accounts.models import UserProfile
from django.http import JsonResponse

@login_required
def shop_page(request):
    user_profile = request.user.profile

    badges = Badge.objects.filter(purchasable=True).exclude(id__in=user_profile.badges.values('id')).order_by('price')

    context = {
        'badges': badges
    }

    return render(request, 'shop.html', context)

def purchase_badge(request, name):
    if request.method == "POST":
        profile = request.user.profile
        badge = Badge.objects.get(name=name)

        if badge in profile.badges.all():
            return JsonResponse({"success": False, "message": "You already own this badge!"})

        if badge.purchasable and profile.points >= badge.price:
            profile.badges.add(badge)
            profile.points -= badge.price
            profile.save()

            return JsonResponse({"success": True, "message": "Badge purchased! 🎉"})
        else:
            return JsonResponse({"success": False, "message": "You do not have enough points to purchase this badge!"})
    
    return JsonResponse({"success": False, "message": "Invalid request"})


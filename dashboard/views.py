from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_page(request):
    user_profile = request.user.profile

    challenges = user_profile.challenges_completed.all()
    quizzes = user_profile.quizzes_completed.all()
    badges = user_profile.badges.all()

    context = {
        'challenges': challenges,
        'quizzes': quizzes,
        'profile': user_profile,
        'badges': badges
    }

    return render(request, 'dashboard.html', context)

def profile_view(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

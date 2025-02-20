from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_page(request):
    return render(request, 'dashboard.html')

def profile_view(request):
    return render(request, 'dashboard.html', {'username': request.user.username})

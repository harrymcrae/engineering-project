from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import  login
from .models import UserProfile

def authView(request): # view for the registration form
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid(): # check if the form is valid
            user = form.save()

            if not hasattr(user, 'profile'): # check if the user has a profile
                UserProfile.objects.create(user=user)

            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})
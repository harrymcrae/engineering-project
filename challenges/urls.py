from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.challenges_page),
    path('claim-registration-bonus/', views.claim_registration_bonus, name='claim_registration_bonus'),
    path('check-registration-bonus/', views.check_registration_bonus_claimed, name='check_registration_bonus_claimed'),
]
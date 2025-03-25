from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.challenges_page),
    path('claim-registration-bonus/', views.claim_registration_bonus, name='claim_registration_bonus'),
    path('check-registration-bonus/', views.check_registration_bonus_claimed, name='check_registration_bonus_claimed'),
    path('claim-daily-bonus/', views.claim_daily_bonus, name='claim_daily_bonus'),
    path('quiz-reward/<str:quiz_id>/', views.quiz_reward, name='quiz_reward'),
    path('check-quiz-completed/<str:quiz_id>/', views.check_quiz_completed, name='check_quiz_completed'),
    path('challenge-reward/<str:challenge_id>/', views.challenge_reward, name='challenge_reward'),
    path('check-challenge-completed/<str:challenge_id>/', views.check_challenge_completed, name='check_challenge_completed'),
    path('submit-proof/<str:challenge_id>/', views.submit_proof, name='submit_proof'),
    path('check-has-submission/<str:challenge_id>/', views.check_has_submission, name='check_has_submission'),
    path('submission-reward/<str:challenge_id>/', views.submission_reward, name='submission_reward'),
]
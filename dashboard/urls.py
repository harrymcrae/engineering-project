from django.urls import path
from .views import dashboard_page
from . import views

urlpatterns = [
    path('', dashboard_page, name='dashboard'),
    path('achievement-reward/<int:achievement_id>/', views.achievement_reward, name='achievement_reward'),
    path('check-achievement-completed/<int:achievement_id>/', views.check_achievement_completed, name='check_achievement_completed')
]
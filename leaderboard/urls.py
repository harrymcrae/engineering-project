from django.urls import path
from .views import leaderboard_page

urlpatterns = [
    path('', leaderboard_page, name='leaderboard'),
]
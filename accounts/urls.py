from django.urls import path, include
from . import views
from dashboard import views as dviews

urlpatterns = [
    path('register/', views.authView),
    path('dashboard/', dviews.dashboard_page),
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.authView),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard),
]
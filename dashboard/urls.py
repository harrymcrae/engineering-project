from django.urls import path
from . import views
from .views import dashboard_page

urlpatterns = [
    path('', dashboard_page, name='dashboard'),
]
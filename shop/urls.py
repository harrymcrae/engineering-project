from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_page, name='shop'),
    path('purchase-badge/<str:name>/', views.purchase_badge, name='purchase_badge'),
]
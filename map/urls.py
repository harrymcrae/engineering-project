from django.urls import path
from .views import map_view, geojson_data

urlpatterns = [
    path('', map_view, name='map'),
    path('geojson/', geojson_data, name='geojson_data'),
]
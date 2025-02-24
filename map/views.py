from django.http import JsonResponse
from challenges.models import Challenge 
from django.shortcuts import render

def map_view(request):
    return render(request, 'map.html')
    # Example GeoJSON data (store in a database in a real project)

def geojson_data(request):
    challengeslist = Challenge.objects.all()
    features = []

    for challenge in challengeslist:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [challenge.longitude, challenge.latitude]
            },
            "properties": {
                "name": challenge.challenge_name,
                "description": challenge.challenge_description,
                "points": challenge.points_awarded
            }
        })

    data = {
        "type": "FeatureCollection",
        "features": features
    }
    return JsonResponse(data)


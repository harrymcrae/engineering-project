from django.http import JsonResponse
from challenges.models import Challenge 
from django.shortcuts import render

def map_view(request):
    return render(request, 'map.html')
    # Example GeoJSON data (store in a database in a real project)

def geojson_data(request):
    challengeslist = Challenge.objects.all()
    user_profile = request.user.profile
    features = []

    for challenge in challengeslist:
        is_completed = challenge in user_profile.challenges_completed.all()
        if not is_completed:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [challenge.longitude, challenge.latitude]
                },
                "properties": {
                    "name": challenge.challenge_name,
                    "description": challenge.challenge_description,
                    "points": challenge.points_awarded,
                    "is_completed": is_completed
                }
            })

    data = {
        "type": "FeatureCollection",
        "features": features
    }
    return JsonResponse(data)


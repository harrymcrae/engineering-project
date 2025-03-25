from django.http import JsonResponse
from challenges.models import Challenge 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def map_view(request): 
    return render(request, 'map.html')
    # Example GeoJSON data (store in a database in a real project)

def geojson_data(request): # This function will return the GeoJSON data for the map
    challengeslist = Challenge.objects.all() # Get all challenges
    user_profile = request.user.profile
    features = []

    for challenge in challengeslist: # Loop through all challenges
        is_completed = challenge in user_profile.challenges_completed.all()
        if not is_completed:
            features.append({ # Append the GeoJSON data to the features list
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [challenge.longitude, challenge.latitude]
                },
                "properties": { # Properties of the GeoJSON data
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


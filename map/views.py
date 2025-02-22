from django.http import JsonResponse
from django.shortcuts import render

def map_view(request):
    return render(request, 'map.html')
    # Example GeoJSON data (store in a database in a real project)
def geojson_data(request):
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-3.537005,50.737556]},
                "properties": {
                    "name": "Sports Park",
                    "description": "Russell Seal Fitness Centre.",
                    "image": "https://www.graingearchitects.co.uk/app/uploads/09-891-Exeter-Uni-Sports-Park-085-1.jpg",
                    "link": "https://example.com"
                }
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point","coordinates": [-3.533572,50.735234]},
                "properties": {
                    "name": "Forum",
                    "description": "Centre for learning",
                    "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTeoU87g3mu5WNdt8uB9CYuSQG9giauJ1TrQ&s",
                    "link": "https://example.com",
                }
            }
            
        ]
    }
    return JsonResponse(data)


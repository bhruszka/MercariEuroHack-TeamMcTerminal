from carpooling.celery import app
from googlemaps.distance_matrix import distance_matrix
import googlemaps
from django.conf import settings


@app.task
def calculate_distances(location_id):
    from carpool_matcher.models import Location, Distance

    location = Location.objects.get(pk=location_id)

    gclient = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    location_objects = Location.objects.filter(pk__lt=location.pk)

    if location_objects:
        locations = [l.get_location_tuple for l in location_objects]

        distance_matrix_response = distance_matrix(gclient, location.get_location_tuple, locations)
        assert distance_matrix_response['status'] == 'OK', 'Bad response from google maps API:\n{}'.format(distance_matrix_response)

        elements = distance_matrix_response['rows'][0]['elements']
        for i, l in enumerate(location_objects):
            distance = elements[i]['distance']['value']
            duration = elements[i]['duration']['value']

            Distance.objects.create(
                start_point=location,
                end_point=l,
                distance=distance,
                time=duration,
            )

    location.all_distances_calculated = True
    location.save()

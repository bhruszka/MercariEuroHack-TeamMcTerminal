from core.models import CommonModel
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from matcher.jobs import calculate_distances


class Location(CommonModel):
    longitude = models.CharField(max_length=15)
    latitude = models.CharField(max_length=15)

    all_distances_calculated = models.BooleanField(default=False)
    order_in_route = models.IntegerField(default=0)

    @property
    def get_location_tuple(self):
        return self.latitude, self.longitude

    @property
    def distances(self):
        return self._start_distances.all() + self._end_distances.all()

    @property
    def routes(self):
        return self._start_routes.all() + self._end_routes.all()

    @staticmethod
    def create_from_string(val):
        lat, long = val.split(', ')
        loc = Location(latitude=lat, longitude=long)
        loc.save()
        return loc

    @staticmethod
    def all_distances_ready():
        return not bool(Location.objects.filter(all_distances_calculated=False))

    class DistancesNotCalculatedException(Exception):
        pass


class DistanceCache:
    class CacheMissException(Exception):
        pass

    def __init__(self):
        if not Location.all_distances_calculated:
            raise Location.DistancesNotCalculatedException()

        distances = Distance.objects.all()

        self._distances = {}

        for distance in distances:
            key = distance.start_point.latitude + distance.start_point.longitude + \
                  distance.end_point.latitude + distance.end_point.longitude
            self._distances[key] = distance

    def get_distance(self, loc1, loc2):
        key1 = loc1.latitude + loc1.longitude + loc2.latitude + loc2.longitude
        key2 = loc2.latitude + loc2.longitude + loc1.latitude + loc1.longitude

        if key1 in self._distances:
            return self._distances[key1]
        elif key2 in self._distances:
            return self._distances[key2]

        raise DistanceCache.CacheMissException()


# @receiver(post_save, sender=Location)
# def location_saved(sender, instance, created, **kwargs):
#     if created:
#         this is a newly created location
#         calculate_distances.delay(instance.pk)


class Distance(CommonModel):
    start_point = models.ForeignKey(Location, models.CASCADE, related_name='_start_distances')
    end_point = models.ForeignKey(Location, models.CASCADE, related_name='_end_distances')

    distance = models.IntegerField()
    time = models.IntegerField()


class Driver(CommonModel):
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name='drivers')

    capacity = models.IntegerField(default=4)

    @property
    def path(self):
        path = []

        d_route = self.routes.first()
        path.append(d_route.start_point)
        path.append(d_route.end_point)

        passengers = self.passengers.all()
        for passenger in passengers:
            p_route = passenger.routes.first()
            path.append(p_route.start_point)
            path.append(p_route.end_point)

        path.sort(key=lambda x: x.order_in_route)
        return path


class Passenger(CommonModel):
    user = models.ForeignKey(get_user_model(), models.CASCADE, related_name='passengers')
    driver = models.ForeignKey(Driver, models.CASCADE, related_name='passengers', null=True)

    @property
    def path(self):
        if not self.driver:
            return []
        driver_path = self.driver.path

        route = self.routes.first()
        start_point = route.start_point
        end_point = route.end_point

        return driver_path[driver_path.index(start_point):driver_path.index(end_point)+1]


class Route(CommonModel):
    start_point = models.ForeignKey(Location, models.CASCADE, related_name='_start_routes')
    end_point = models.ForeignKey(Location, models.CASCADE, related_name='_end_routes')

    distance = models.IntegerField(null=True)
    time = models.IntegerField(null=True)

    driver = models.ForeignKey(Driver, models.CASCADE, related_name='routes', null=True)
    passenger = models.ForeignKey(Passenger, models.CASCADE, related_name='routes', null=True)

    @staticmethod
    def create_route(start_latlng, end_latlng, user, role):
        route = Route()
        if role == 'driver':
            route.driver = Driver.objects.create(user=user)
        elif role == 'passenger':
            route.passenger = Passenger.objects.create(user=user)
        else:
            raise Exception('No role given.')
        route.start_point = Location.create_from_string(start_latlng)
        route.end_point = Location.create_from_string(end_latlng)
        route.save()
        return route



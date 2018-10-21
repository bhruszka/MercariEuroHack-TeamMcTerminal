from googlemaps.directions import directions
import googlemaps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from carpool_matcher.models import Location, DistanceCache, Distance, DistanceCache, Passenger, Driver
import random


def modified_dijkstra_search(driver, passengers, distance_cache=None, full=True):
    if distance_cache is None:
        distance_cache = DistanceCache()

    d_route = driver.routes.first()
    node_map = {
        0: d_route.start_point,
        1: d_route.end_point,
    }

    for i, passenger in enumerate(passengers, start=2):
        p_route = passenger.routes.first()
        node_map[i] = p_route.start_point
        node_map[i + len(passengers)] = p_route.end_point

    class Path:
        def __init__(self, path=None, cost=0):
            self.path = list(path) or []
            self.path_set = set(self.path)
            self.cost = cost

        def check_feasibility(self, node):
            if node in self.path_set or node == 0:
                return False

            if node != 1 and node >= len(passengers) + 2 and node - len(passengers) not in self.path_set:
                return False

            if node == 1 and len(self.path) < len(passengers) + 1:
                return False

            return True

        def append_node(self, node):
            # assume feasible
            self.cost += distance_cache.get_distance(node_map[self.path[-1]], node_map[node]).time
            self.path.append(node)
            self.path_set.add(node)

        @staticmethod
        def copy_and_append(from_path, node):
            new_path = Path(path=from_path.path, cost=from_path.cost)
            new_path.append_node(node)
            return new_path

    paths = [Path(path=[0])]

    lowest_cost_path = paths[0]

    if full:
        while len(lowest_cost_path.path) != 2*len(passengers) + 2:
            feasible_nodes = []
            for node in range(1, 2 * len(passengers) + 2):
                if lowest_cost_path.check_feasibility(node):
                    feasible_nodes.append(node)

            for node in feasible_nodes[1:]:
                paths.append(Path.copy_and_append(lowest_cost_path, node))
            lowest_cost_path.append_node(feasible_nodes[0])

            lowest_cost_path = min(paths, key=lambda x: x.cost)
    else:
        while len(lowest_cost_path.path) != 2*len(passengers) + 2:
            # feasible_nodes = []
            new_paths = []
            for node in range(1, 2 * len(passengers) + 2):
                if lowest_cost_path.check_feasibility(node):
                    # feasible_nodes.append((node, distance_cache.get_distance(node_map[lowest_cost_path.path[-1]],
                    #                                                          node_map[node]).time))
                    new_paths.append(Path.copy_and_append(lowest_cost_path, node))
            # lowest_cost_path.append_node(min(feasible_nodes, key=lambda x: x[1])[0])
            lowest_cost_path = min(new_paths, key=lambda x: x.cost)

    return [node_map[node] for node in lowest_cost_path.path], lowest_cost_path.cost


def get_polyline_from_path(path):
    gclient = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    return directions(gclient, path[0].get_location_tuple, path[-1].get_location_tuple,
                      waypoints=[p.get_location_tuple for p in path[1:-2]])[0]['overview_polyline']['points']


MAX_VALUE = 9999999999


def match_all_passengers():
    if not Location.all_distances_calculated:
        raise CommandError('Not all distances calculated.')

    dc = DistanceCache()

    Passenger.objects.all().update(driver=None)
    Location.objects.all().update(order_in_route=0)

    passengers = list(Passenger.objects.all())
    drivers = list(Driver.objects.all())
    extramileage = {}

    # start PHASE 1

    for driver in drivers:
        route = driver.routes.first()
        driver.distance = dc.get_distance(route.start_point, route.end_point)
        driver._passengers = []
        driver._passenger_count = 0

    def add_passenger(_driver, _passenger):
        _driver._passengers.append(_passenger)
        _driver._passenger_count += 1

    def remove_passenger(_driver, _passenger):
        _driver._passengers.remove(_passenger)
        _driver._passenger_count -= 1

    for passenger in passengers:
        _extramileage = []
        p_route = passenger.routes.first()
        for driver in drivers:
            d_route = driver.routes.first()
            _extramileage.append(
                (
                    driver,
                    dc.get_distance(d_route.start_point, p_route.start_point).time +
                    dc.get_distance(p_route.start_point, p_route.end_point).time +
                    dc.get_distance(p_route.end_point, d_route.end_point).time -
                    driver.distance.time
                )
            )
        _extramileage.sort(key=lambda x: x[1])

        if len(_extramileage) > 1:
            passenger.regret = _extramileage[1][1] - _extramileage[0][1]
        elif len(_extramileage) == 1:
            passenger.regret = _extramileage[0][1]
        else:
            passenger.regret = MAX_VALUE

        extramileage[passenger.pk] = _extramileage

    passengers.sort(key=lambda x: x.regret, reverse=True)
    unassigned_passengers = []

    for passenger in passengers:
        feasible_drivers = extramileage.get(passenger.pk, [])
        for driver, cost in feasible_drivers:
            if driver._passenger_count < driver.capacity - 1:
                add_passenger(driver, passenger)
                break
        else:
            unassigned_passengers.append(passenger)

    # start PHASE 2
    def stop_condition(_drivers, _passengers):
        for _driver in _drivers:
            if not _driver._passengers:
                return False
        else:
            return True

    loops = 0
    while loops < 10 and not stop_condition(drivers, passengers):
        for driver in drivers:
            if driver._passengers:
                passenger_to_remove = random.choice(driver._passengers)
                remove_passenger(driver, passenger_to_remove)
                unassigned_passengers.append(passenger_to_remove)

            _, driver.time = modified_dijkstra_search(driver, driver._passengers, distance_cache=dc, full=False)

        for passenger in unassigned_passengers:
            _extramileage = []
            for driver in drivers:
                _, cost = modified_dijkstra_search(driver, driver._passengers + [passenger], distance_cache=dc, full=False)
                _extramileage.append(
                    (
                        driver,
                        cost - driver.time
                    )
                )
            _extramileage.sort(key=lambda x: x[1])

            if len(_extramileage) > 1:
                passenger.regret = _extramileage[1][1] - _extramileage[0][1]
            elif len(_extramileage) == 1:
                passenger.regret = _extramileage[0][1]
            else:
                passenger.regret = MAX_VALUE

            extramileage[passenger.pk] = _extramileage

        unassigned_passengers.sort(key=lambda x: x.regret, reverse=True)

        for passenger in unassigned_passengers:
            feasible_drivers = extramileage.get(passenger.pk, [])
            for driver, cost in feasible_drivers:
                if driver._passenger_count < driver.capacity - 1:
                    add_passenger(driver, passenger)
                    unassigned_passengers.remove(passenger)
                    break

    for passenger in unassigned_passengers:
        feasible_drivers = extramileage.get(passenger.pk, [])
        for driver, cost in feasible_drivers:
            if driver._passenger_count < driver.capacity - 1:
                add_passenger(driver, passenger)
                unassigned_passengers.remove(passenger)
                break

    for driver in drivers:
        for passenger in driver._passengers:
            passenger.driver = driver
            passenger.save()

        path, cost = modified_dijkstra_search(driver, driver._passengers, distance_cache=dc)

        for i, location in enumerate(path):
            location.order_in_route = i
            location.save()

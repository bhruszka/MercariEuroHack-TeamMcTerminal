import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from carpool_matcher.factories import UserFactory
from carpool_matcher.models import Location, Distance, DistanceCache, Passenger, Driver, Route
from carpool_matcher.utils import modified_dijkstra_search
import random

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        self.users = []
        self.drivers = []
        self.passengers = []
        self.routes = []
        super(Command, self).__init__(*args, **kwargs)

    def _make_users(self, options):
        users = UserFactory.create_batch(size=23)
        for user in users:
            user.set_password('test')
            user.save()

        self.users = users

    def _make_routes(self, options):
        from_points = [
            {
                'point_1': [52.145362, 21.018677],
                'point_2': [52.155426, 21.051561],
            },
            {
                'point_1': [52.149375, 20.913649],
                'point_2': [52.157047, 20.956858],
            },
            {
                'point_1': [52.162907, 20.852725],
                'point_2': [52.180820, 20.898751],
            },
        ]
        to_points = {
            'point_1': [52.219624, 20.991787],
            'point_2': [52.232035, 21.024743]
        }

        routes = []
        count = 0
        for user in self.users:
            if count % 4 == 0:
                role = 'driver'
            else:
                role = 'passenger'

            from_point = random.choice(from_points)
            start_latlng = "{}, {}".format(
                float(
                    random.randrange(
                        from_point['point_1'][0] * 1000000,
                        from_point['point_2'][0] * 1000000
                    )
                ) / 1000000,
                float(
                    random.randrange(
                        from_point['point_1'][1] * 1000000,
                        from_point['point_2'][1] * 1000000
                    )
                ) / 1000000
            )
            end_latlng = "{}, {}".format(
                float(
                    random.randrange(
                        to_points['point_1'][0] * 1000000,
                        to_points['point_2'][0] * 1000000
                    )
                ) / 1000000,
                float(
                    random.randrange(
                        to_points['point_1'][1] * 1000000,
                        to_points['point_2'][1] * 1000000
                    )
                ) / 1000000
            )
            routes.append(
                Route.create_route(start_latlng=start_latlng, end_latlng=end_latlng, role=role,
                                   user=user))
            count += 1
        self.routes = routes

    def handle(self, *args, **options):
        print("Prepare to populate DB")

        # Creating users block
        print("USER - create...")
        self._make_users(options=options)
        print("Created {count} users".format(count=len(self.users)))

        print("ROUTE - create...")
        self._make_routes(options=options)
        print("Created {count} route".format(count=len(self.routes)))

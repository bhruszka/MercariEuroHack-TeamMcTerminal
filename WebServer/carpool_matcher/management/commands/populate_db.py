import logging

from django.contrib.auth import get_user_model
from django.core.files import File
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
        avatars = [
            '5cvJHVrz.jpg',
            '21.jpg',
            'AEF44435-B547-4B84-A2AE-887DFAEE6DDF-200w.jpeg',
            'EBYH22-K.jpg',
            'female-14.jpeg',
            'female-59.jpg',
            'male-47.jpg',
            'MV5BMDc2M2NkMTctNmQ0MS00MjQxLWFkMGItNGY1Y2Y3NzYzZjg1XkEyXkFqcGdeQXVyNjAzMTgxNjY@._V1_UY256_CR74,0,172,256_AL_.jpg',
            'MV5BMjE5ODk2NTI2Nl5BMl5BanBnXkFtZTgwNzIyMDA4MTE@._V1_UY256_CR6,0,172,256_AL_.jpg',
            'noplz47r59v1uxvyg8ku.png',
            'oedmUmVc.jpg',
            'pexels-photo-247917.jpeg',
            'pexels-photo-274595.jpeg',
            'photo-1463453091185-61582044d556.jpg',
            'photo-1502980426475-b83966705988.jpg',
            'rSuiu_Hr.jpg'
        ]

        users = UserFactory.create_batch(size=12)
        for user in users:
            user.set_password('test')
            image_name = avatars.pop()
            reopen = open("media/faces/{}".format(image_name), 'rb')
            file = File(reopen)
            user.save()
            user.avatar.save(image_name, file, save=True)

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

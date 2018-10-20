import logging

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from carpool_matcher.jobs import calculate_distances
        from carpool_matcher.models import Location

        uncalculated_locations = Location.objects.filter(all_distances_calculated=False)

        logger.warning('START calculating all missing distances')

        for i, location in enumerate(uncalculated_locations):
            calculate_distances(location.pk)
            logger.warning('PROGRESS {}/{}'.format(i+1, len(uncalculated_locations)))

        logger.warning('DONE calculating all missing distances')


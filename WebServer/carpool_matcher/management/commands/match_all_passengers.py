import logging

from django.core.management import BaseCommand

from carpool_matcher.utils import match_all_passengers


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info('START passenger matching.')
        match_all_passengers()
        logger.info('DONE passenger matching.')


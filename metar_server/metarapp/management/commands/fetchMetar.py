from django.core.management.base import BaseCommand
from typing import Any, Optional
from metar_server.metarapp.myfunction import metar_function


class Command(BaseCommand):
    help = 'Fetch METAR data and save to database.'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Command of fetching and saving METARs.

        Returns:
            Optional[str]: Options for inherited function.
        """
        airport_list = metar_function.get_airport_list()
        metar_input = metar_function.MetarInput(airport_list)
        metar_input.fetch_and_save()
        self.stdout.write('Fetched airport is %s' % airport_list)
        self.stdout.write('Fetched time is %s' % metar_input.fetched_time)
        return super().handle(*args, **options)

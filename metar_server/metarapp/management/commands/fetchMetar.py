from django.core.management.base import BaseCommand
from typing import Any, Optional
from metar_server.metarapp.models import Airport, Metar
from metar_server.metarapp.myfunction import metar_function


class Command(BaseCommand):
    help = 'Fetch METAR data and save to database.'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        airport_list_query = Airport.objects \
            .filter(
                is_fetched=True
            ) \
            .values_list('station_id')
        airport_list = list(airport_list_query)
        metar_input = metar_function.MetarInput(airport_list)
        self.stdout.write('Fetched airport is %s' % airport_list)
        self.stdout.write('Fetched time is %s' % metar_input.fetched_time)
        return super().handle(*args, **options)
